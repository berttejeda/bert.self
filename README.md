# bert.self

Source for [bertdotself.com](https://bertdotself.com), the personal site of Bert Tejeda:
a professional portfolio plus my technical notes and lessons.

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

## Contact

[GitHub](https://github.com/berttejeda) ·
[LinkedIn](https://www.linkedin.com/in/engelberttejeda/) ·
[berttejeda@gmail.com](mailto:berttejeda@gmail.com)
