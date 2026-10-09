---
name: publish-site
description: Publish the bert.self MkDocs site to GitHub Pages (the gh-pages branch, served at https://berttejeda.github.io/bert.self/, with bertdotself.com redirecting there). Runs pre-deploy checks, deploys with mkdocs gh-deploy after explicit user confirmation, then verifies the live site. Use when asked to publish, deploy, release or push the site live, or to update GitHub Pages.
---

# Publish the site to GitHub Pages

## How hosting works

- **Pages source:** GitHub Pages serves the root of the **`gh-pages`** branch of
  `berttejeda/bert.self` in legacy "deploy from a branch" mode. There is no Actions workflow.
- **What `gh-pages` holds:** only built output. Never edit it or merge it with `main`.
- **URL:** <https://berttejeda.github.io/bert.self/>. `bertdotself.com` is a Squarespace domain
  that 301-redirects there. There's no `CNAME` and no custom domain in Pages, so don't add one.
- **Deploy tool:** `mkdocs gh-deploy`. It wraps `ghp-import`: it builds `site/`, commits it as a
  new commit on top of the existing `gh-pages` history (replacing the whole tree and adding
  `.nojekyll`) and pushes to `origin`.

Publishing is outward-facing: it changes a public website. **Never run the deploy without
the user's explicit go-ahead in this conversation**, even when the checks pass.

## Workflow

### 1. Preflight

```bash
.claude/skills/publish-site/scripts/preflight.sh
```

The script pushes nothing. It checks:

- **Source state:** on `main`, tracked files clean, in sync with `origin/main`. It
  fast-forwards a stale local `gh-pages`.
- **Lessons:** `../bert.lessons` is present and current.
- **Build:** `mkdocs build` passes with no new warnings. The `crossplane.io` warnings from
  upstream lessons are known and ignored.
- **Output:**
  - no unresolved `external_markdown` includes ("File not found");
  - no tooling files (`.py`, `.pyc`, `Dockerfile`, `requirements.txt`, `README`) in `site/`;
  - the canonical URL matches `site_url`.

If anything fails, fix it, or tell the user what's blocking and stop. Common fixes:

| Failure | Fix |
|---|---|
| Uncommitted changes | Ask whether to commit them first. Don't deploy a dirty tree: the deploy message names a sha that wouldn't match what's published. |
| Not on `main` | Deploy from `main`. Use `--allow-branch` only if the user explicitly asks to publish a branch. |
| HEAD ≠ `origin/main` | Ask before pushing `main`, so the deployed sha is public. |
| `../bert.lessons` missing or stale | `git clone https://github.com/berttejeda/bert.lessons.git ../bert.lessons`, or `git -C ../bert.lessons pull --ff-only` |
| Unresolved includes | A lesson stub points at content that's missing in `bert.lessons`. Take the page out of `nav` and add it to `exclude_docs` in `mkdocs.yml`. |
| Tooling files in `site/` | Add the pattern to `exclude_docs` in `mkdocs.yml`. `docs_dir` is the repo root, so everything not excluded gets published. |

### 2. Show what will change, then ask

Summarize for the user:

- the `main` commit being deployed (`git log -1 --oneline`);
- what's live now (`git log -1 --format='%s (%cs)' origin/gh-pages`);
- the size of the new build, from the preflight `info` lines (file count and size);
- notable content changes since the last deploy:

    ```bash
    git log --oneline <deployed-sha>..HEAD
    ```

    Get the deployed sha from the `gh-pages` commit message. The legacy "Refreshed site"
    deploys don't record one, so for those, summarize from the date instead.

Then ask: "Publish this to https://berttejeda.github.io/bert.self/?" Wait for a clear yes.

### 3. Deploy

```bash
DISABLE_MKDOCS_2_WARNING=true .venv/bin/mkdocs gh-deploy -m "Deploy {sha} with MkDocs {version}"
```

Don't pass `--force` or `--no-history` unless the user asks. Both rewrite the public branch
history. If the push is rejected because the remote moved, fetch, rerun preflight and ask again.

If `gh-deploy` refuses because the last deploy used a newer MkDocs version, tell the user.
Pass `--ignore-version` only if they agree.

### 4. Verify the live site

Pages usually rebuilds within one to two minutes. Poll the build status, without tight loops:

```bash
gh api repos/berttejeda/bert.self/pages/builds/latest --jq '{status, commit, error: .error.message}'
```

Once `status` is `built` and `commit` matches the new `origin/gh-pages` sha, check:

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://berttejeda.github.io/bert.self/
```

```bash
curl -sL https://berttejeda.github.io/bert.self/ | grep -o '<title>[^<]*'
```

```bash
curl -sIL https://bertdotself.com | grep -iE '^(HTTP|location)'
```

Optionally open the live URL in the browser preview and screenshot the home page.

### 5. Report

Say:

- which `main` sha is now live, and the `gh-pages` commit;
- the live URL;
- the Pages build status;
- anything skipped or overridden.

## Rolling back

When the user asks to roll back, choose one of these:

- **Re-deploy an older version:** check out an older `main` commit and rerun steps 1–4. Use
  `--allow-branch` for preflight, since that's a detached HEAD. Then switch back to `main`.
- **Revert on `gh-pages`:** this needs confirmation, since it pushes:

    ```bash
    git switch gh-pages && git revert --no-edit HEAD && git push origin gh-pages && git switch main
    ```

## Background

Until 2026, deploys were done by hand: build, copy `site/` onto `gh-pages`, commit
"Refreshed site". Those deploys also leaked `docs/macros.py` and `__pycache__`, which is why
the preflight checks for tooling files. `gh-deploy` continues on that same branch history.
