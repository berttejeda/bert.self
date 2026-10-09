#!/usr/bin/env bash
# Pre-deploy checks for publishing bert.self to GitHub Pages.
# Builds the site into site/ and fails (non-zero) if anything would publish a broken site.
# Pushes nothing.
#
# Usage: preflight.sh [--allow-branch]   (--allow-branch permits deploying from a branch other than main)

set -uo pipefail

repo_root=$(git rev-parse --show-toplevel) || exit 1
cd "$repo_root" || exit 1

allow_branch=false
[[ "${1:-}" == "--allow-branch" ]] && allow_branch=true

mkdocs=.venv/bin/mkdocs
[[ -x $mkdocs ]] || mkdocs=$(command -v mkdocs)

failures=0
pass() { printf '  ok    %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; failures=$((failures + 1)); }
info() { printf '  info  %s\n' "$1"; }

echo "Source"
branch=$(git rev-parse --abbrev-ref HEAD)
if [[ $branch == main ]]; then pass "on main"
elif $allow_branch; then info "deploying from branch '$branch' (--allow-branch)"
else fail "on '$branch', not main (switch to main, or pass --allow-branch)"
fi

if [[ -z $(git status --porcelain --untracked-files=no) ]]; then pass "no uncommitted changes to tracked files"
else fail "uncommitted changes; the deploy commit message would name a sha that doesn't match what's published"
fi

git fetch -q origin "$branch" gh-pages 2>/dev/null
if [[ $(git rev-parse HEAD) == $(git rev-parse "origin/$branch" 2>/dev/null) ]]; then pass "in sync with origin/$branch"
else info "HEAD differs from origin/$branch (unpushed or behind); push main first so the deployed sha is public"
fi

if git show-ref -q refs/heads/gh-pages && [[ $(git rev-parse gh-pages) != $(git rev-parse origin/gh-pages) ]]; then
  if git merge-base --is-ancestor gh-pages origin/gh-pages; then
    info "local gh-pages is behind origin; fast-forwarding it"
    git branch -f gh-pages origin/gh-pages >/dev/null
  else
    fail "local gh-pages has commits not on origin/gh-pages; inspect before deploying"
  fi
fi
info "live deploy: $(git log -1 --format='%s (%cs)' origin/gh-pages 2>/dev/null)"

echo "Content dependencies"
lessons="$repo_root/../bert.lessons"
if [[ -d $lessons/.git ]]; then
  git -C "$lessons" fetch -q origin 2>/dev/null
  if [[ $(git -C "$lessons" rev-parse HEAD) == $(git -C "$lessons" rev-parse '@{u}' 2>/dev/null) ]]; then
    pass "../bert.lessons present and current"
  else
    info "../bert.lessons is not at its upstream (run: git -C ../bert.lessons pull --ff-only)"
  fi
else
  fail "../bert.lessons missing (run: git clone https://github.com/berttejeda/bert.lessons.git ../bert.lessons)"
fi

echo "Build"
build_log=$(DISABLE_MKDOCS_2_WARNING=true "$mkdocs" build --clean 2>&1)
if [[ $? -eq 0 ]]; then pass "mkdocs build succeeded"
else fail "mkdocs build failed"; echo "$build_log" | tail -20
fi

# Known upstream warning: bert.lessons links to 'crossplane.io' without a scheme
warnings=$(echo "$build_log" | grep -E '^(WARNING|ERROR)' | grep -v "crossplane.io")
if [[ -z $warnings ]]; then pass "no new build warnings"
else fail "build warnings:"; echo "$warnings" | sed 's/^/        /'
fi

if [[ -f site/index.html ]]; then
  missing=$(grep -rl "File not found" site --include=index.html)
  if [[ -z $missing ]]; then pass "all external_markdown includes resolved"
  else fail "pages with unresolved includes:"; echo "$missing" | sed 's/^/        /'
  fi

  leaked=$(find site \( -name '*.py' -o -name '*.pyc' -o -name 'Dockerfile' -o -name 'requirements.txt' -o -name 'README*' \) | head)
  if [[ -z $leaked ]]; then pass "no source/tooling files in site/"
  else fail "tooling files would be published:"; echo "$leaked" | sed 's/^/        /'
  fi

  site_url=$(grep -E '^site_url:' mkdocs.yml | awk '{print $2}')
  if grep -q "rel=\"canonical\" href=\"$site_url" site/index.html; then pass "canonical URL is $site_url"
  else fail "canonical URL in site/index.html doesn't match site_url ($site_url)"
  fi
  info "site/ contains $(find site -type f | wc -l | tr -d ' ') files, $(du -sh site | cut -f1)"
fi

echo
if (( failures )); then echo "PREFLIGHT FAILED ($failures)"; exit 1; fi
echo "PREFLIGHT PASSED — ready to run: $mkdocs gh-deploy -m \"Deploy {sha} with MkDocs {version}\""
