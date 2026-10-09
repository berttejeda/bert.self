# bert.self

Source for [bertdotself.com](https://bertdotself.com), the personal site of Bert Tejeda:
a professional portfolio plus my technical notes and lessons.

The site is hosted on GitHub Pages at <https://berttejeda.github.io/bert.self/>.
`bertdotself.com` is registered with Squarespace and redirects there.

It's built with [MkDocs](https://www.mkdocs.org/) and the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.

## Site contents

| Page | Source | What it covers |
|---|---|---|
| Home | [index.md](index.md) | Summary, highlights, featured projects and skills |
| Projects | [docs/projects.md](docs/projects.md) | Open-source portfolio grouped by theme |
| Activity | [docs/activity.md](docs/activity.md) | Year-by-year GitHub contribution timeline |
| Notes | [docs/notes.md](docs/notes.md), [docs/topics/](docs/topics) | Lessons and troubleshooting write-ups |

This `README.md` is excluded from the site build (`exclude_docs` in [mkdocs.yml](mkdocs.yml)),
so it only documents the repository.

## Quick start

Requires Python 3.9+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Preview locally with live reload at <http://localhost:8000>:

```bash
mkdocs serve
```

Build the static site into `site/`:

```bash
mkdocs build
```

### Docker

The image under [docs/](docs) installs the same requirements and runs `mkdocs serve`:

```bash
docker build -t bert.self -f docs/Dockerfile docs
```

```bash
docker run --rm -p 8000:8000 -v "$PWD":/docs -v "$PWD/../bert.lessons":/bert.lessons bert.self
```

## Publishing to GitHub Pages

### How hosting is set up

- **Pages source:** GitHub Pages serves the root of the **`gh-pages`** branch in
  "Deploy from a branch" mode (*Settings → Pages*). There is no Actions workflow.
- **What `gh-pages` holds:** only the built static site. Never edit it by hand.
- **Domain:** there's no custom domain, so there's no `CNAME` file. `bertdotself.com` reaches the
  site through a Squarespace redirect, which is managed in Squarespace, not here.
- **`site_url`:** it's set in [mkdocs.yml](mkdocs.yml) to the github.io URL, so the sitemap and
  canonical links match where the site is actually served.

### Deploy

Publish from an up-to-date `main` with a clean working tree:

```bash
git switch main && git pull --ff-only
```

Make sure the [bert.lessons](#lessons-from-bertlessons) checkout is present and current.
Otherwise the lesson pages will publish as "File not found":

```bash
git -C ../bert.lessons pull --ff-only
```

Build once to check for errors before anything is pushed:

```bash
mkdocs build
```

Then deploy:

```bash
mkdocs gh-deploy -m "Deploy {sha} with MkDocs {version}"
```

`mkdocs gh-deploy` does the following:

1. Rebuilds `site/` from a clean state.
2. Commits it to the local `gh-pages` branch as a new commit on top of the existing history,
   replacing the whole tree and adding `.nojekyll`. `{sha}` in the message expands to the
   `main` commit that was deployed.
3. Pushes `gh-pages` to `origin`.

GitHub Pages usually rebuilds within a minute or two. To check the Pages build status:

```bash
gh api repos/berttejeda/bert.self/pages --jq .status
```

To see which `main` commit is live:

```bash
git log -1 --format=%s origin/gh-pages
```

### Rolling back

Re-deploy an older version by checking out that commit of `main` and running `gh-deploy`
again. Alternatively, revert the latest commit on `gh-pages` and push it:

```bash
git switch gh-pages && git revert --no-edit HEAD && git push origin gh-pages && git switch main
```

### History

Before 2026, deploys were done by hand: build `site/`, copy it onto the `gh-pages` branch and
commit it as "Refreshed site". Those deploys also published build tooling, such as
`docs/macros.py` and `__pycache__`. Those files are now kept out with `exclude_docs`.
`mkdocs gh-deploy` replaces that manual process and builds on the same branch history.

## Lessons from bert.lessons

The lesson pages under `docs/topics/*/lesson-*/` are stubs that pull their content from a
sibling checkout of [bert.lessons](https://github.com/berttejeda/bert.lessons) at build time,
using the `external_markdown` macro in [docs/macros.py](docs/macros.py):

```text
git/self/
├── bert.self/      # this repo
└── bert.lessons/   # required for lesson pages to render
```

```bash
git clone https://github.com/berttejeda/bert.lessons.git ../bert.lessons
```

Without that checkout, the build still succeeds, but lesson pages show a "File not found" message.

## Project layout

```text
.
├── index.md            # site home page
├── mkdocs.yml          # site config, theme and navigation
├── requirements.txt    # Python dependencies (also copied to docs/requirements.txt for Docker)
└── docs/
    ├── projects.md     # portfolio
    ├── activity.md     # contribution timeline
    ├── notes.md        # notes landing page
    ├── topics/         # notes and lesson stubs, by topic
    ├── tutorial/       # notes on MkDocs itself
    ├── macros.py       # mkdocs-macros: external_markdown, cheat_page, video, etc.
    └── theme/          # logo and optional CSS/JS assets
```

## Maintenance notes

- **Stay on MkDocs 1.x.** MkDocs 2.0 removes the plugin and theme system this site relies on,
  so `requirements.txt` pins `mkdocs<2`. To hide Material's upgrade warning, set
  `DISABLE_MKDOCS_2_WARNING=true`.
- **Adding a page.** Create the Markdown file and add it under `nav:` in `mkdocs.yml`.
  Pages missing from `nav` still build, but they're hidden from the menus.
- **Refreshing portfolio stats.** The figures in `index.md`, `docs/projects.md` and
  `docs/activity.md` came from the GitHub API and PyPI, and are current as of October 2026.
  For example:

    ```bash
    gh repo list berttejeda --limit 300 --source --json name,stargazerCount,pushedAt
    ```

- **`cheat_page` macro.** It needs the Bootstrap/DataTables assets in `docs/theme/`. These
  aren't loaded globally because they override Material's styles, so include them only on
  pages that use the macro.

## Agent skills

Two Claude Code skills in [.claude/skills/](.claude/skills) automate upkeep:

- **[refresh-portfolio](.claude/skills/refresh-portfolio/SKILL.md)** re-collects GitHub and PyPI
  data and updates `index.md`, `docs/projects.md` and `docs/activity.md`.
- **[publish-site](.claude/skills/publish-site/SKILL.md)** runs the pre-deploy checks in
  [scripts/preflight.sh](.claude/skills/publish-site/scripts/preflight.sh), deploys with
  `mkdocs gh-deploy` once you confirm, and verifies the live site.

You can also run the preflight on its own before a manual deploy:

```bash
.claude/skills/publish-site/scripts/preflight.sh
```

## Contact

[GitHub](https://github.com/berttejeda) ·
[LinkedIn](https://www.linkedin.com/in/engelberttejeda/) ·
[berttejeda@gmail.com](mailto:berttejeda@gmail.com)
