---
name: refresh-portfolio
description: Refresh the bert.self MkDocs portfolio site (index.md, docs/projects.md, docs/activity.md, README.md) from Bert's live GitHub commit history, repositories and PyPI packages, then build and visually verify it. Use when asked to update the site or README with recent work, activity, projects or stats, to "refresh the portfolio", or when the site's numbers look stale.
---

# Refresh the portfolio site

This repo is an MkDocs + Material site whose portfolio pages are written from real GitHub and
PyPI data. This skill re-collects that data, updates the pages so every claim stays true,
and proves the site still builds and renders.

## Files this skill owns

| File | Role | What gets refreshed |
|---|---|---|
| `index.md` | Site home page | "At a glance" stat cards, the four "Featured work" cards, "Core skills" tabs, "Currently" list |
| `docs/projects.md` | Portfolio | Project tables by theme: description, stack, commits, releases, stars |
| `docs/activity.md` | Contribution timeline | Yearly table, "How the work has evolved" narrative, "By the numbers" table, "Data as of" date |
| `docs/notes.md` | Notes landing page | Only if lesson topics change in `bert.lessons` |
| `mkdocs.yml` | Config and nav | Only `nav:` (new or removed pages) |
| `README.md` | Repo docs, excluded from the site build | Site-contents table and any changed build steps. No portfolio stats go here. |

Leave `docs/topics/**`, `docs/tutorial/**` and `docs/macros.py` alone unless the build needs it.

## Workflow

### 1. Collect data

```bash
python3 .claude/skills/refresh-portfolio/scripts/collect.py --out "$SCRATCH/portfolio.json"
```

`$SCRATCH` is the session scratchpad. The script needs an authenticated `gh` and takes about
90 seconds. It writes:

- `user`: the GitHub profile.
- `yearly_activity[]`: contributions, commits and PRs per year, plus `commits_by_repo`.
- `repos[]`: every public, non-fork repo, with these fields:
  - `default_branch_commits`, `stars`, `created`, `last_push`, `archived`
  - `languages`, `top_level_files`, `readme_excerpt`
  - `pypi`, including `verified_owner`
- `summary`: repo counts, verified PyPI packages and release total, top repos by commits,
  language mix.

If it misses a PyPI package, rerun it with `--extra-pypi repo-name=package-name`.

Read the JSON with `jq` instead of printing all of it. For example:

```bash
jq '.summary' portfolio.json
jq -c '.yearly_activity[] | {year, total_contributions, commits_by_repo}' portfolio.json
jq -r '.repos[] | [.name, .default_branch_commits, .last_push, (.description // "")] | @tsv' portfolio.json
```

### 2. Diff against the current pages

Read `index.md`, `docs/projects.md` and `docs/activity.md`, and list what's stale:

- Numbers that changed: repo count, PyPI packages and releases, commit totals, yearly figures.
- New or newly active repos that aren't listed. Check `last_push` and the current year's
  `commits_by_repo`.
- Repos that have been archived or superseded.
- Whether the current year's leading projects still match "Currently" and the 2025–present
  narrative.

Tell the user briefly what you plan to change before you rewrite anything substantial.

### 3. Verify before you describe anything

**Every project description must be grounded in that repo's own content, not its name.**

- Start with `readme_excerpt` and `top_level_files`. If a repo has no README, inspect its tree:

    ```bash
    gh api 'repos/berttejeda/<repo>/git/trees/HEAD?recursive=1' --jq '[.tree[].path]|join(" ")'
    ```

- Names mislead. In the first pass, `terraform-aws-sentinel` looked like HashiCorp Sentinel
  policies, but it actually ships AWS CloudTrail logs to Microsoft Sentinel.
  `bert.ansible.collection.utilities` turned out to contain just one inventory plugin.
- GitHub's language label can be wrong, too. `bert.validator` is tagged JavaScript but is a Go tool.
- Count a PyPI package only when `pypi.verified_owner` is true.
- Don't invent employers, job titles, dates, metrics or certifications. The repos don't show
  work history. Link to LinkedIn for that.
- When you're unsure, describe the project less and link to it.

### 4. Write the pages

Follow the existing structure and voice: plain, specific, first person, not salesy.

- **Stats.** Round down to defensible figures ("60+ original repositories", "120+ releases").
  Use the same numbers on `index.md` and `docs/activity.md`.
- **Activity table.** Include the counts in the Focus column (`repo (N)`), and update
  "Data as of <Month YYYY>".
  - Keep the admonition explaining that contribution counts leave out commits from unlinked
    emails. That's why yearly numbers can be lower than per-repo totals.
  - For years with tiny contribution counts, name repos that were created or pushed in that
    year (from `created`/`last_push`), not just the ones the contribution graph reports.
- **Featured work.** Exactly four cards, each with a description and stack tags. Prefer
  projects that are both substantial (commits/releases) and recently active.
- **Projects tables.** Keep the themed sections and add new sections only when a new theme
  appears. Every row links to the repo, and to PyPI when published.
- **Material features.** These are already enabled: grid cards (`<div class="grid cards" markdown>`),
  admonitions, content tabs (`=== "Tab"`) and icons (`:material-...:`, `:simple-...:`,
  `:fontawesome-...:`).

### 5. Build

```bash
.venv/bin/mkdocs build 2>&1 | grep -E "^WARNING|ERROR|built in"
```

If `.venv` is missing, create it first with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.

The build must have no new warnings or errors. These three are known and harmless:
`crossplane.io` link warnings that come from upstream `bert.lessons` content.

Lesson pages need `../bert.lessons` checked out next to this repo. If it's missing, run
`git clone https://github.com/berttejeda/bert.lessons.git ../bert.lessons`.

### 6. Check the rendering

Run `.claude/launch.json` (`mkdocs serve`) with the browser preview, then screenshot Home,
Projects and Activity at desktop width, plus Home at mobile width. Check that cards lay out
in a grid, tables don't overflow and nothing renders as raw Markdown. Stop the server when
you're done.

### 7. Report

Summarize what changed: numbers before and after, projects added or removed, and anything you
couldn't verify. Don't commit unless the user asks.

## Known pitfalls (already fixed; don't reintroduce them)

- **Stay on MkDocs 1.x.** `requirements.txt` pins `mkdocs<2`. Keep `docs/requirements.txt`
  identical, since the Docker image uses it.
- **Abandoned packages.** Don't add `markdown-blockdiag`. It imports the removed
  `markdown.util.etree` and breaks the build.
- **Unused plugins.** Don't add plugins or extensions that no page uses, and install anything
  you do add.
- **Bootstrap.** Don't load Bootstrap/DataTables globally through `extra_css`/`extra_javascript`.
  It overrides Material's styles (underlined links, broken cards).
- **Macros.** In `docs/macros.py`, macros must be registered from `define_env`. The legacy
  `declare_variables` hook only runs because `define_env` calls it.
- **Home page.** The home page is `index.md`. `README.md` is excluded via `exclude_docs`, so
  don't point nav at it.
- **Lesson stubs.** Pages under `docs/topics/*/lesson-*/` only render if their source exists
  in `bert.lessons`. The Docker lessons were once live with no committed source, and had to be
  recovered from the `gh-pages` HTML in 2026. Commit lesson content to `bert.lessons` first.
