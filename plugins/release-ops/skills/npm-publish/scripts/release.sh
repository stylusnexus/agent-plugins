#!/usr/bin/env bash
# Release: commit and push. Does NOT publish — the agent calls publish.sh
# separately so it can orchestrate auth recovery if needed.
#
# Two runs, with the user's confirmation in between:
#   release.sh [--access public]            print the plan (files, commit, branch); change nothing
#   release.sh --confirm [--access public]  commit those files and push
#
# Only the release files are committed (package.json, CHANGELOG.md,
# .claude-plugin/plugin.json, site/index.html). Other changed files are listed
# and left alone; it never runs git add -u or git add -A.
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

VERSION=$(node -p 'require("./package.json").version')
PKG_NAME=$(node -p 'require("./package.json").name')
BRANCH=$(git branch --show-current)

RELEASE_FILES=""
for f in package.json CHANGELOG.md .claude-plugin/plugin.json site/index.html; do
  [ -f "$f" ] || continue
  if [ -n "$(git status --porcelain -- "$f")" ]; then
    RELEASE_FILES="$RELEASE_FILES $f"
  fi
done

if [ "$CONFIRMED" != true ]; then
  echo "RELEASE_PLAN:$PKG_NAME:$VERSION:$BRANCH"
  echo "Commit message: Release v$VERSION"
  echo "Files to commit:${RELEASE_FILES:- (none)}"
  OTHER=""
  while read -r f; do
    [ -n "$f" ] || continue
    if ! printf ' %s ' "$RELEASE_FILES" | grep -q -F " $f "; then
      OTHER="$OTHER  $f
"
    fi
  done <<EOF
$(git status --porcelain | awk '{print $NF}')
EOF
  OTHER="${OTHER%
}"
  if [ -n "$OTHER" ]; then
    echo "Not committed (left as they are):"
    echo "$OTHER"
  fi
  echo "Push to: origin/$BRANCH"
  echo "CONFIRM_PUSH"
  exit 0
fi

echo "Committing v$VERSION..."
if [ -z "$RELEASE_FILES" ]; then
  echo "Nothing to commit."
else
  # shellcheck disable=SC2086 # RELEASE_FILES is a space-separated list of fixed names
  git add -- $RELEASE_FILES
  echo "Staged:$RELEASE_FILES"
  git commit -m "Release v$VERSION" -- $RELEASE_FILES
fi

# Push
echo "Pushing to $BRANCH..."
git push origin "$BRANCH"

echo "RELEASE_DONE:$PKG_NAME:$VERSION:$EXTRA_FLAGS"
