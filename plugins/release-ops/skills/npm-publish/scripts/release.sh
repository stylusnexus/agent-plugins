#!/usr/bin/env bash
# Release: commit and push. Does NOT publish — the agent calls publish.sh
# separately so it can orchestrate auth recovery if needed.
#
# Two runs, with the user's confirmation in between:
#   release.sh [--access public]            print the plan (files, commit, branch); change nothing
#   release.sh --confirm [--access public]  commit those files and push
#
# Only the release files are committed: package.json, CHANGELOG.md,
# .claude-plugin/plugin.json, site/index.html and the lockfiles. It never runs
# git add -u or git add -A. Any other tracked change (source edits, build
# output from preflight) would be published without being committed, so both
# runs stop with DIRTY_TREE and list those files instead.
# Usage: release.sh [--confirm] [--access public] [--dry-run]
set -euo pipefail

# Pass-through flags (stored for the agent to use with publish.sh)
EXTRA_FLAGS=""
CONFIRMED=false
while [ $# -gt 0 ]; do
  case "$1" in
    --access) EXTRA_FLAGS="--access $2"; shift 2 ;;
    --dry-run) EXTRA_FLAGS="--dry-run"; shift ;;
    --confirm) CONFIRMED=true; shift ;;
    *) shift ;;
  esac
done

# Read one package.json field with node, or bun when node is missing.
pkg_field() {
  if command -v node >/dev/null 2>&1; then
    node -p "require('./package.json').$1"
  elif command -v bun >/dev/null 2>&1; then
    bun -e "console.log(require('./package.json').$1)"
  else
    echo "NODE_REQUIRED" >&2
    exit 1
  fi
}

VERSION=$(pkg_field version)
PKG_NAME=$(pkg_field name)
BRANCH=$(git branch --show-current)

ALLOWED=(package.json CHANGELOG.md .claude-plugin/plugin.json site/index.html
  package-lock.json npm-shrinkwrap.json bun.lock bun.lockb yarn.lock pnpm-lock.yaml)

is_release_file() {
  local f
  for f in "${ALLOWED[@]}"; do
    [ "$1" = "$f" ] && return 0
  done
  return 1
}

RELEASE_FILES=()
for f in "${ALLOWED[@]}"; do
  [ -f "$f" ] || continue
  if [ -n "$(git status --porcelain -- "$f")" ]; then
    RELEASE_FILES+=("$f")
  fi
done

# Tracked files changed outside the release files (untracked files are not listed).
DIRTY=()
while IFS= read -r f; do
  [ -n "$f" ] || continue
  is_release_file "$f" || DIRTY+=("$f")
done <<EOF
$(git status --porcelain --untracked-files=no | awk '{print $NF}')
EOF

if [ "${#DIRTY[@]}" -gt 0 ]; then
  echo "DIRTY_TREE"
  echo "Tracked files changed outside the release files (they would be published but not committed):"
  printf '  %s\n' "${DIRTY[@]}"
  echo "Commit, stash or revert them, then run release.sh again."
  exit 1
fi

if [ "$CONFIRMED" != true ]; then
  echo "RELEASE_PLAN:$PKG_NAME:$VERSION:$BRANCH"
  echo "Commit message: Release v$VERSION"
  if [ "${#RELEASE_FILES[@]}" -gt 0 ]; then
    echo "Files to commit: ${RELEASE_FILES[*]}"
  else
    echo "Files to commit: (none)"
  fi
  echo "Push to: origin/$BRANCH"
  echo "CONFIRM_PUSH"
  exit 0
fi

echo "Committing v$VERSION..."
if [ "${#RELEASE_FILES[@]}" -eq 0 ]; then
  echo "Nothing to commit."
else
  git add -- "${RELEASE_FILES[@]}"
  echo "Staged: ${RELEASE_FILES[*]}"
  git commit -m "Release v$VERSION" -- "${RELEASE_FILES[@]}"
fi

# Push
echo "Pushing to $BRANCH..."
git push origin "$BRANCH"

echo "RELEASE_DONE:$PKG_NAME:$VERSION:$EXTRA_FLAGS"
