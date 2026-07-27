#!/usr/bin/env sh
# Fail if the two marketplace manifests disagree. Claude Code reads
# .claude-plugin/marketplace.json; Codex reads .agents/plugins/marketplace.json. They
# use different source shapes but MUST agree on which plugins exist and where each one
# is pinned — otherwise a release silently ships to one harness and not the other
# (defect-scan was invisible in Codex this way; see stylusnexus/defect-scan#45).
#
# Two hosting modes, each with a per-harness shape:
#   external repo   Claude {source:github, repo, ref}      Codex {source:url, url, ref}
#   in-repo plugin  Claude "./plugins/<name>"  (a string)  Codex {source:local, path}
# Both are reduced to a comparable pin: "ref:<tag>" or "local:<path>".
set -eu
C=.claude-plugin/marketplace.json
A=.agents/plugins/marketplace.json
for f in "$C" "$A"; do [ -f "$f" ] || { echo "missing manifest: $f" >&2; exit 2; }; done

PIN='.plugins[]|select(.name==$n)|
  if   (.source|type) == "string" then "local:" + (.source|sub("^\\./";""))
  elif (.source.ref // "") != ""  then "ref:"   + .source.ref
  elif (.source.path // "") != "" then "local:" + (.source.path|sub("^\\./";""))
  else "MISSING" end'

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
  cr=$(jq -r --arg n "$name" "$PIN" "$C")
  ar=$(jq -r --arg n "$name" "$PIN" "$A")
  if [ "$cr" != "$ar" ]; then
    echo "MISMATCH: '$name' pin differs — .claude-plugin=$cr  .agents=$ar" >&2
    fail=1
    continue
  fi
  # An in-repo plugin must actually exist and carry a manifest for each harness,
  # or the entry points at nothing.
  case "$cr" in
    local:*)
      dir=${cr#local:}
      [ -d "$dir" ] || { echo "MISSING: '$name' points at absent directory '$dir'" >&2; fail=1; continue; }
      for m in .claude-plugin/plugin.json .codex-plugin/plugin.json; do
        [ -f "$dir/$m" ] || { echo "MISSING: '$name' has no $m (needed by that harness)" >&2; fail=1; }
      done
      ;;
  esac
done

[ "$fail" = 0 ] && echo "manifests in sync (same plugins, matching pins, in-repo plugins resolve)"
exit "$fail"
