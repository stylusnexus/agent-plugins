#!/usr/bin/env sh
# Fail if the two marketplace manifests disagree. Claude Code reads
# .claude-plugin/marketplace.json; Codex reads .agents/plugins/marketplace.json. They
# use different source shapes (github+repo vs url+.git) but MUST agree on which plugins
# exist and each plugin's pinned `ref` — otherwise a release silently ships to one
# harness and not the other (defect-scan was invisible in Codex this way; see
# stylusnexus/defect-scan#45).
set -eu
C=.claude-plugin/marketplace.json
A=.agents/plugins/marketplace.json
for f in "$C" "$A"; do [ -f "$f" ] || { echo "missing manifest: $f" >&2; exit 2; }; done
fail=0
cn=$(jq -r '.plugins[].name' "$C" | sort)
an=$(jq -r '.plugins[].name' "$A" | sort)
if [ "$cn" != "$an" ]; then
  echo "MISMATCH: plugin sets differ." >&2
  echo "  .claude-plugin: $(echo "$cn" | tr '\n' ' ')" >&2
  echo "  .agents:        $(echo "$an" | tr '\n' ' ')" >&2
  fail=1
fi
for name in $cn; do
  echo "$an" | grep -qx "$name" || continue
  cr=$(jq -r --arg n "$name" '.plugins[]|select(.name==$n)|.source.ref // "MISSING"' "$C")
  ar=$(jq -r --arg n "$name" '.plugins[]|select(.name==$n)|.source.ref // "MISSING"' "$A")
  if [ "$cr" != "$ar" ]; then
    echo "MISMATCH: '$name' ref differs — .claude-plugin=$cr  .agents=$ar" >&2
    fail=1
  fi
done
[ "$fail" = 0 ] && echo "manifests in sync (same plugins, matching refs)"
exit "$fail"
