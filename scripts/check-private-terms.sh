#!/usr/bin/env sh
# Fail the build if a skill or agent file ships an owner-private name: a
# personal name, a private/dormant Stylus Nexus product, an internal
# filesystem path, a secrets-adjacent filename, or an unrelated company that
# has no business in this PUBLIC MIT marketplace's shipped text.
#
# Scope is plugins/*/skills/**, plugins/*/agents/**, and plugins/*/README.md.
# plugin.json and LICENSE are never scanned -- the publisher name there is
# legitimate and the whole point of the LICENSE file.
#
# "Stylus Nexus" is a narrower case: it's also the publisher name on every
# plugin README.md's copyright line ("MIT (c) Stylus Nexus Holdings LLC"),
# which is legitimate there the same way it is in LICENSE. So that one
# pattern is scanned only against skills/**and agents/**, not README.md --
# every other pattern covers all three.
#
# Matching is case-insensitive, so "example" also catches "Example" --
# no need for separate-case duplicates in any denylist.
#
# The denylist itself is layered, because this script's own source and
# scripts/private-terms.txt are both public and committed:
#   1. scripts/private-terms.txt   -- public terms/patterns (committed).
#   2. scripts/private-terms.local.txt -- the owner's private overlay
#      (gitignored, not committed; absent for forks and fresh clones).
#   3. $PRIVATE_TERMS env var      -- newline-separated regexes, set as a
#      repository secret for CI on the owner's own pushes/PRs. Empty on
#      fork PRs, which then run with the public list only.
#
# Warning tier: an overlay line that starts with "warn:" is a warning, not a
# failure. It is for a private product's VOCABULARY (its domain nouns), which
# names miss: a worked example lifted from the product can leak it without
# naming it. Some of those words are also ordinary English, so a hit asks a
# person to look rather than blocking the PR. In GitHub Actions each hit
# becomes a ::warning annotation on the PR (file and line only); locally the
# matching line is printed too, since a local terminal is private. Warning
# patterns never run against docs/.
#
# One extra check: docs/ (internal planning material, never shipped) is
# scanned against ONLY the local/secret overlay, never the public list --
# docs/ legitimately discusses the owner's private products by name, so the
# public denylist would false-positive there. Without an overlay (no local
# file, no env var) there's nothing private to check docs/ against, so that
# check is skipped with a notice.
set -eu

HERE=$(dirname "$0")
DENYLIST="$HERE/private-terms.txt"
LOCAL_DENYLIST="$HERE/private-terms.local.txt"
[ -f "$DENYLIST" ] || { echo "missing denylist: $DENYLIST" >&2; exit 2; }

PATTERNS_FILE=$(mktemp)
OVERLAY_FILE=$(mktemp)
SCAN_LIST_ALL=$(mktemp)
SCAN_LIST_NO_README=$(mktemp)
trap 'rm -f "$PATTERNS_FILE" "$OVERLAY_FILE" "$SCAN_LIST_ALL" "$SCAN_LIST_NO_README"' EXIT

cat "$DENYLIST" > "$PATTERNS_FILE"
echo >> "$PATTERNS_FILE"

if [ -f "$LOCAL_DENYLIST" ]; then
  echo "using local private-terms overlay: $LOCAL_DENYLIST" >&2
  cat "$LOCAL_DENYLIST" >> "$OVERLAY_FILE"
  echo >> "$OVERLAY_FILE"
fi

if [ -n "${PRIVATE_TERMS:-}" ]; then
  echo "using PRIVATE_TERMS env overlay" >&2
  printf '%s\n' "$PRIVATE_TERMS" >> "$OVERLAY_FILE"
else
  echo "PRIVATE_TERMS not set -- scanning with the public denylist only (expected on fork PRs, which don't get repo secrets)" >&2
fi

cat "$OVERLAY_FILE" >> "$PATTERNS_FILE"

fail=0
warned=0

report_warning() {
  # $1 = grep hits (file:line:text), never echoed to CI logs with the text
  echo "$1" | while IFS= read -r hit; do
    file=$(echo "$hit" | cut -d: -f1)
    line=$(echo "$hit" | cut -d: -f2)
    if [ "${GITHUB_ACTIONS:-}" = "true" ]; then
      echo "::warning file=$file,line=$line::Possible private-product vocabulary (from the private list). Check this line was not lifted from a private product."
    else
      echo "  $hit" >&2
    fi
  done
}

: > "$SCAN_LIST_ALL"
: > "$SCAN_LIST_NO_README"
if [ -d plugins ]; then
  find plugins -type d \( -name skills -o -name agents \) -print0 > "$SCAN_LIST_NO_README" 2>/dev/null || true
  cat "$SCAN_LIST_NO_README" > "$SCAN_LIST_ALL"
  find plugins -mindepth 2 -maxdepth 2 -type f -name README.md -print0 >> "$SCAN_LIST_ALL" 2>/dev/null || true
fi

if [ -s "$SCAN_LIST_ALL" ]; then
  while IFS= read -r pattern; do
    case "$pattern" in
      ''|'#'*) continue ;;
      warn:*)
        hits=$(xargs -0 grep -rniIE "${pattern#warn:}" < "$SCAN_LIST_ALL" 2>/dev/null || true)
        if [ -n "$hits" ]; then
          echo "WARNING: private-product vocabulary (from the private list) found; check these lines:" >&2
          report_warning "$hits"
          warned=1
        fi
        continue ;;
    esac
    if [ "$pattern" = "Stylus Nexus" ]; then
      scan_list="$SCAN_LIST_NO_README"
    else
      scan_list="$SCAN_LIST_ALL"
    fi
    [ -s "$scan_list" ] || continue
    hits=$(xargs -0 grep -rniIE "$pattern" < "$scan_list" 2>/dev/null || true)
    if [ -n "$hits" ]; then
      if grep -Fxq -- "$pattern" "$DENYLIST"; then
        echo "PRIVATE TERM '$pattern' found:" >&2
        echo "$hits" | sed 's/^/  /' >&2
      else
        # Overlay terms are private: CI logs on a public repo are public, so
        # report only file:line -- never the term or the matching text.
        echo "PRIVATE TERM (from the private list) found at:" >&2
        echo "$hits" | cut -d: -f1,2 | sed 's/^/  /' >&2
      fi
      fail=1
    fi
  done < "$PATTERNS_FILE"
else
  echo "no plugins/*/skills, plugins/*/agents, or plugin README.md found -- nothing to scan" >&2
fi

# Targeted docs/ check: overlay-only (see header) -- the owner's private
# terms must never appear outside her own private repos, but docs/
# legitimately names her private products elsewhere.
if [ -d docs ] && [ -s "$OVERLAY_FILE" ]; then
  while IFS= read -r pattern; do
    case "$pattern" in
      ''|'#'*) continue ;;
    esac
    case "$pattern" in warn:*) continue ;; esac
    hits=$(grep -rniIE "$pattern" docs 2>/dev/null || true)
    if [ -n "$hits" ]; then
      echo "PRIVATE TERM (from the private list) found in docs/ at:" >&2
      echo "$hits" | cut -d: -f1,2 | sed 's/^/  /' >&2
      fail=1
    fi
  done < "$OVERLAY_FILE"
elif [ -d docs ]; then
  echo "no private-terms overlay available -- skipping docs/ check" >&2
fi

[ "$warned" = 1 ] && echo "warnings above are not failures: confirm each line is generic, or rewrite it" >&2
[ "$fail" = 0 ] && echo "no private terms found in plugins/*/skills, plugins/*/agents, plugins/*/README.md, or docs/"
exit "$fail"
