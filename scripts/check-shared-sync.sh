#!/usr/bin/env sh
# Fail if a bundled copy of a shared file has drifted from its canonical source.
#
# Some skills carry their own copy of a file that another skill or a plugin
# agent owns, so a single-skill install (Skills CLI --skill, a Claude app ZIP)
# still has everything the SKILL.md reads:
#
#   product-manager/references/principles.md  -> every pm-* skill's references/
#   marketing-lead/references/principles.md   -> six mk-* skills' references/
#   agents/audience-scout.md (body only)      -> mk-audience/references/audience-scout-brief.md
#
# Edit the canonical file, then copy it over each listed copy (the brief keeps
# its title and one-paragraph header; its body is the agent file minus the
# frontmatter). This check compares them byte for byte so a change to one side
# cannot ship without the other.
set -eu

fail=0

same() {
  # same <canonical> <copy>
  if [ ! -f "$1" ]; then echo "missing canonical file: $1" >&2; fail=1; return; fi
  if [ ! -f "$2" ]; then echo "missing copy: $2 (copy it from $1)" >&2; fail=1; return; fi
  if ! cmp -s "$1" "$2"; then
    echo "out of sync: $2 differs from $1 (copy the canonical file over it)" >&2
    fail=1
  fi
}

PM=plugins/product-strategy/skills/product-manager/references/principles.md
for s in pm-canvas pm-capabilities pm-discovery pm-growth pm-market-analysis pm-objectives \
         pm-roadmap pm-strategy pm-strategy-fit pm-teams pm-value-proposition pm-vision pm-visuals; do
  same "$PM" "plugins/product-strategy/skills/$s/references/principles.md"
done

MK=plugins/go-to-market/skills/marketing-lead/references/principles.md
for s in mk-copy mk-founder-content mk-launch mk-lifecycle mk-outreach mk-search; do
  same "$MK" "plugins/go-to-market/skills/$s/references/principles.md"
done

# The brief is the agent file minus its frontmatter, under a fixed two-line header.
AGENT=plugins/go-to-market/agents/audience-scout.md
BRIEF=plugins/go-to-market/skills/mk-audience/references/audience-scout-brief.md
if [ ! -f "$AGENT" ] || [ ! -f "$BRIEF" ]; then
  echo "missing $AGENT or $BRIEF" >&2; fail=1
else
  tmp_agent=$(mktemp); tmp_brief=$(mktemp)
  # body of the agent: everything after the second --- line
  awk 'f>=2{print} /^---$/{f++}' "$AGENT" | sed '/./,$!d' >"$tmp_agent"
  # body of the brief: everything after its title and one-paragraph header (two blank lines)
  awk 'f>=2{print} /^$/{f++}' "$BRIEF" | sed '/./,$!d' >"$tmp_brief"
  if ! cmp -s "$tmp_agent" "$tmp_brief"; then
    echo "out of sync: $BRIEF body differs from $AGENT body (paste the agent body under the brief's header)" >&2
    fail=1
  fi
  rm -f "$tmp_agent" "$tmp_brief"
fi

if [ "$fail" -ne 0 ]; then
  echo "check-shared-sync: FAIL" >&2
  exit 1
fi
echo "check-shared-sync: every bundled copy matches its canonical file"
