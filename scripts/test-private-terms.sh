#!/usr/bin/env sh
# The exact public marketplace attribution is allowed in README.md, but the
# same term must still fail elsewhere in public pages and shipped skill text.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
CHECK_SH=$(command -v dash || command -v sh)

mkdir -p "$TMP/scripts" "$TMP/plugins/example/skills"
cp "$ROOT/scripts/check-private-terms.sh" "$TMP/scripts/"
printf '# test denylist\n' > "$TMP/scripts/private-terms.txt"
awk '/^Eve McGivern, who maintains these packs, also publishes a personal marketplace,/{copy=1} copy && NF == 0{exit} copy{print}' \
  "$ROOT/README.md" > "$TMP/README.md"

if (cd "$TMP" && PRIVATE_TERMS='Eve McGivern|evemcgivern' \
    "$CHECK_SH" "$TMP/scripts/check-private-terms.sh" > "$TMP/allowed.out" 2>&1); then
  :
else
  cat "$TMP/allowed.out" >&2
  echo "exact public marketplace attribution should be allowed" >&2
  exit 1
fi

printf '\nUnreviewed reference: Eve McGivern\n' >> "$TMP/README.md"
if (cd "$TMP" && PRIVATE_TERMS='Eve McGivern|evemcgivern' \
    "$CHECK_SH" "$TMP/scripts/check-private-terms.sh" > "$TMP/readme-leak.out" 2>&1); then
  echo "unreviewed README reference should fail" >&2
  exit 1
fi
grep -q 'README.md:' "$TMP/readme-leak.out"
if grep -Eq 'Eve McGivern|evemcgivern' "$TMP/readme-leak.out"; then
  echo "scanner output exposed the private-term match" >&2
  exit 1
fi

awk '/^Eve McGivern, who maintains these packs, also publishes a personal marketplace,/{copy=1} copy && NF == 0{exit} copy{print}' \
  "$ROOT/README.md" > "$TMP/README.md"
mkdir -p "$TMP/site"
printf 'Eve McGivern\n' > "$TMP/site/page.html"
printf 'Eve McGivern\n' > "$TMP/plugins/example/skills/SKILL.md"
if (cd "$TMP" && PRIVATE_TERMS='Eve McGivern|evemcgivern' \
    "$CHECK_SH" "$TMP/scripts/check-private-terms.sh" > "$TMP/other-leaks.out" 2>&1); then
  echo "Pages site and skill text should still be scanned" >&2
  exit 1
fi
grep -q 'site/page.html:' "$TMP/other-leaks.out"
grep -q 'plugins/example/skills' "$TMP/other-leaks.out"
if grep -Eq 'Eve McGivern|evemcgivern' "$TMP/other-leaks.out"; then
  echo "scanner output exposed the private-term match" >&2
  exit 1
fi

echo "private-term scanner keeps the public-reference exception narrow"
