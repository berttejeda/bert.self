#!/usr/bin/env python3
"""Collect GitHub + PyPI portfolio data for a user into one JSON file.

Uses the authenticated `gh` CLI (no tokens handled here) and PyPI's public JSON API.
Standard library only.

Usage:
    collect.py --out portfolio.json [--user LOGIN] [--since-year 2019] [--readme-lines 40]
               [--extra-pypi REPO=PACKAGE ...] [--author NAME_OR_EMAIL ...]
"""
import argparse
import base64
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request


def gh(*args, check=True):
    proc = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout if proc.returncode == 0 else None


def gh_json(*args, check=True):
    out = gh(*args, check=check)
    return json.loads(out) if out else None


def graphql(query, **variables):
    args = ["api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        args += ["-F", f"{key}={value}"]
    return gh_json(*args)["data"]


def current_user():
    return gh_json("api", "user")["login"]


def profile(user):
    data = gh_json("api", f"users/{user}")
    keys = ("login", "name", "bio", "blog", "company", "location", "public_repos", "followers", "created_at")
    return {k: data.get(k) for k in keys}


def repos(user):
    fields = ("name,description,primaryLanguage,stargazerCount,forkCount,isFork,isArchived,"
              "isPrivate,pushedAt,createdAt,repositoryTopics,url,homepageUrl")
    return gh_json("repo", "list", user, "--limit", "1000", "--json", fields)


COMMIT_TOTALS = """
query($login:String!, $endCursor:String) {
  user(login:$login) {
    repositories(first:100, after:$endCursor, ownerAffiliations:OWNER, isFork:false) {
      pageInfo { hasNextPage endCursor }
      nodes { name defaultBranchRef { target { ... on Commit { history { totalCount } } } } }
    }
  }
}"""


def commit_totals(user):
    totals, cursor = {}, None
    while True:
        variables = {"login": user}
        if cursor:
            variables["endCursor"] = cursor
        page = graphql(COMMIT_TOTALS, **variables)["user"]["repositories"]
        for node in page["nodes"]:
            ref = node["defaultBranchRef"]
            totals[node["name"]] = ref["target"]["history"]["totalCount"] if ref else 0
        if not page["pageInfo"]["hasNextPage"]:
            return totals
        cursor = page["pageInfo"]["endCursor"]


YEARLY = """
query($login:String!, $from:DateTime!, $to:DateTime!) {
  user(login:$login) {
    contributionsCollection(from:$from, to:$to) {
      totalCommitContributions totalPullRequestContributions totalIssueContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions }
      commitContributionsByRepository(maxRepositories:25) {
        repository { name } contributions { totalCount }
      }
    }
  }
}"""


def yearly_activity(user, since_year):
    years = []
    for year in range(since_year, dt.date.today().year + 1):
        c = graphql(YEARLY, login=user, **{"from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        c = c["user"]["contributionsCollection"]
        years.append({
            "year": year,
            "total_contributions": c["contributionCalendar"]["totalContributions"],
            "commits": c["totalCommitContributions"],
            "pull_requests": c["totalPullRequestContributions"],
            "issues": c["totalIssueContributions"],
            "private_contributions": c["restrictedContributionsCount"],
            "commits_by_repo": {r["repository"]["name"]: r["contributions"]["totalCount"]
                                for r in c["commitContributionsByRepository"]},
        })
    return years


def repo_file(user, repo, path):
    data = gh_json("api", f"repos/{user}/{repo}/contents/{path}", check=False)
    if not data or isinstance(data, list) or "content" not in data:
        return None
    return base64.b64decode(data["content"]).decode("utf-8", errors="replace")


def readme_excerpt(user, repo, max_lines):
    text = gh("api", f"repos/{user}/{repo}/readme", "-H", "Accept: application/vnd.github.raw", check=False)
    if not text:
        return None
    # Drop doctoc TOCs, badges and blank lines so the excerpt is mostly prose
    text = re.sub(r"<!-- START doctoc.*?END doctoc[^>]*-->", "", text, flags=re.S)
    lines = [l for l in text.splitlines()
             if l.strip() and "shields.io" not in l and not l.lstrip().startswith(("![", "<img", "<a name"))]
    return "\n".join(lines[:max_lines])


def top_level_tree(user, repo):
    data = gh_json("api", f"repos/{user}/{repo}/git/trees/HEAD", check=False)
    return [t["path"] for t in data["tree"]] if data else []


def languages(user, repo):
    return list((gh_json("api", f"repos/{user}/{repo}/languages", check=False) or {}).keys())


NAME_PATTERNS = {
    "pyproject.toml": re.compile(r'^\s*name\s*=\s*["\']([^"\']+)["\']', re.M),
    "setup.cfg": re.compile(r'^\s*name\s*=\s*([A-Za-z0-9_.\-]+)\s*$', re.M),   # unquoted INI value
    "setup.py": re.compile(r'\bname\s*=\s*["\']([A-Za-z0-9_.\-]+)["\']'),
}


def python_package_name(user, repo):
    for path, pattern in NAME_PATTERNS.items():
        text = repo_file(user, repo, path)
        match = pattern.search(text) if text else None
        if match:
            return match.group(1)
    return None


def pypi(package, user, owner_names):
    try:
        with urllib.request.urlopen(f"https://pypi.org/pypi/{package}/json", timeout=15) as resp:
            data = json.load(resp)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    info = data["info"]
    links = " ".join(filter(None, [info.get("home_page"), *(info.get("project_urls") or {}).values()]))
    authors = " ".join(filter(None, [info.get(k) for k in ("author", "author_email", "maintainer", "maintainer_email")]))
    releases = {v: files for v, files in data["releases"].items() if files}
    uploads = sorted(f["upload_time"] for files in releases.values() for f in files)
    return {
        "package": data["info"]["name"],
        "version": data["info"]["version"],
        "releases": len(releases),
        "first_release": uploads[0][:10] if uploads else None,
        "last_release": uploads[-1][:10] if uploads else None,
        "url": f"https://pypi.org/project/{data['info']['name']}/",
        # A name match alone could be someone else's package; trust it only if it links back to the
        # user's GitHub or names them as author/maintainer
        "verified_owner": (f"github.com/{user}/".lower() in links.lower()
                           or any(n.lower() in authors.lower() for n in owner_names)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True, help="output JSON path")
    parser.add_argument("--user", help="GitHub login (default: authenticated gh user)")
    parser.add_argument("--since-year", type=int, default=2019)
    parser.add_argument("--readme-lines", type=int, default=40)
    parser.add_argument("--extra-pypi", nargs="*", default=[], metavar="REPO=PACKAGE",
                        help="PyPI packages auto-detection misses, e.g. my-repo=my-package")
    parser.add_argument("--author", nargs="*", default=[],
                        help="extra author names/emails that mark a PyPI package as yours (profile name is always used)")
    args = parser.parse_args()

    user = args.user or current_user()
    log = lambda msg: print(msg, file=sys.stderr)

    log(f"profile + repos for {user}")
    result = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
              "user": profile(user)}
    all_repos = repos(user)
    totals = commit_totals(user)

    log("yearly contributions")
    result["yearly_activity"] = yearly_activity(user, args.since_year)

    owned = [r for r in all_repos if not r["isFork"] and not r["isPrivate"]]
    extra_pypi = dict(item.split("=", 1) for item in args.extra_pypi)
    owner_names = [n for n in (result["user"]["name"], *args.author) if n]
    log(f"inspecting {len(owned)} public original repos")
    detailed = []
    for r in sorted(owned, key=lambda r: r["pushedAt"], reverse=True):
        name = r["name"]
        entry = {
            "name": name,
            "url": r["url"],
            "description": r["description"],
            "primary_language": (r["primaryLanguage"] or {}).get("name"),
            "languages": languages(user, name),
            "topics": [t["name"] for t in (r["repositoryTopics"] or [])],
            "stars": r["stargazerCount"],
            "forks": r["forkCount"],
            "archived": r["isArchived"],
            "created": r["createdAt"][:10],
            "last_push": r["pushedAt"][:10],
            "default_branch_commits": totals.get(name, 0),
            "top_level_files": top_level_tree(user, name),
            "readme_excerpt": readme_excerpt(user, name, args.readme_lines),
        }
        package = extra_pypi.get(name)
        if not package and (entry["primary_language"] == "Python" or "Python" in entry["languages"]):
            package = python_package_name(user, name)
        entry["pypi"] = pypi(package, user, owner_names) if package else None
        detailed.append(entry)
    result["repos"] = detailed

    published = [r["pypi"] for r in detailed if r.get("pypi") and r["pypi"]["verified_owner"]]
    result["summary"] = {
        "public_repos_total": result["user"]["public_repos"],
        "original_public_repos": len(owned),
        "forks": sum(1 for r in all_repos if r["isFork"]),
        "pypi_packages": sorted(p["package"] for p in published),
        "pypi_release_total": sum(p["releases"] for p in published),
        "pypi_unverified": sorted(r["pypi"]["package"] for r in detailed
                                  if r.get("pypi") and not r["pypi"]["verified_owner"]),
        "top_repos_by_commits": sorted(((r["name"], r["default_branch_commits"]) for r in detailed),
                                       key=lambda x: -x[1])[:15],
        "languages_by_repo_count": dict(sorted(
            {lang: sum(1 for r in detailed if r["primary_language"] == lang)
             for lang in {r["primary_language"] for r in detailed if r["primary_language"]}}.items(),
            key=lambda x: -x[1])),
    }

    with open(args.out, "w") as fh:
        json.dump(result, fh, indent=2)
    log(f"wrote {args.out}")


if __name__ == "__main__":
    main()
