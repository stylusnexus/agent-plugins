#!/usr/bin/env bash
# npm-publish: Try publish, output status codes for agent to interpret.
# The agent orchestrates auth recovery — this script just reports status.
# Publishing needs the user's go-ahead: without --confirm it only prints what
# it would publish and exits.
# Usage: publish.sh --confirm [--access public] [--dry-run]
set -uo pipefail

EXTRA_FLAGS=""
CONFIRMED=false
while [ $# -gt 0 ]; do
  case "$1" in
    --access) EXTRA_FLAGS="$EXTRA_FLAGS --access $2"; shift 2 ;;
    --dry-run) EXTRA_FLAGS="$EXTRA_FLAGS --dry-run"; shift ;;
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

# A tracked change that is not committed would be published without being in
# git. Stop and list it instead.
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  DIRTY=$(git status --porcelain --untracked-files=no | awk '{print $NF}')
  if [ -n "$DIRTY" ]; then
    echo "DIRTY_TREE"
    echo "Tracked files with uncommitted changes (they would be published but are not committed):"
    printf '%s\n' "$DIRTY" | sed 's/^/  /'
    echo "Commit, stash or revert them, then run publish.sh again."
    exit 1
  fi
fi

if [ "$CONFIRMED" != true ]; then
  echo "CONFIRM_PUBLISH:$(pkg_field name):$(pkg_field version):${EXTRA_FLAGS# }"
  exit 0
fi

# Try publish — pipe ENTER for OTP browser prompt
OUTPUT=$(echo "" | bun publish $EXTRA_FLAGS 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "$OUTPUT"
  echo "PUBLISH_SUCCESS"
  exit 0
fi

# Check if auth-related failure
if echo "$OUTPUT" | grep -qi "404\|401\|403\|unauthorized\|ENEEDAUTH\|authentication"; then
  echo "AUTH_FAILED"
  exit 1
else
  echo "$OUTPUT"
  echo "PUBLISH_ERROR"
  exit 1
fi
