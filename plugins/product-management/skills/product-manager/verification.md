# Verification

What's actually been checked in this plugin, and what hasn't. Treat anything not listed here as unverified.

## Structure
- 14 skills ship: the chief `product-manager` skill plus 13 focused `pm-*` skills. Two agents ship: `product-manager` and `business-capability-modeler`.
- Every `SKILL.md` and agent file has valid YAML frontmatter with the required `name` and `description` fields — checked by parsing each file's frontmatter block directly rather than assuming it's well-formed.
- Internal Markdown/HTML links inside `skills/product-manager/` (this file's own directory) resolve to real files: `grep`-derived link targets were resolved against the filesystem and confirmed present.

## Scripts
- `scripts/metrics_lookup.py` runs against the bundled `skills/pm-objectives/references/metrics-catalog.json` (40 entries) with no network access and no writes. A smoke query for `activation` returns the expected category entries.
- `scripts/discovery_digest.py` has a real unit test suite at `scripts/tests/test_discovery_digest.py` (3 cases, run with `python3 -m unittest scripts/tests/test_discovery_digest.py`), covering: provenance flags on an incomplete record plus HTML/pipe-safe output escaping; synthetic-research records being rejected unless labeled `synthetic` status; and rejection of duplicate IDs, invalid dates, and unrecognized source types. All three pass.
- Neither script performs network calls, writes files, or mutates anything outside its own return value — both are read-only by construction, not just by convention.

## Templates and sourcing
- `skills/pm-canvas/templates/product-strategy-canvas.md` and `skills/pm-value-proposition/templates/value-proposition.md` are original table/row layouts written for this plugin, built around named public frameworks (Roger Martin and A.G. Lafley's *Playing to Win* choice cascade; Jobs to Be Done and Strategyn's Outcome-Driven Innovation) rather than adapted from any single proprietary template — checked by reading each file directly, including its cited public sources and stated list of what is the framework versus what is this plugin's own addition.
- Every other reference file in the plugin is original text describing publicly documented methods, cited to a primary or official source in `references/sources.md`.

## What has not been independently verified
- No real project's strategy, market position, or product outcomes have been validated by installing or using this plugin — the frameworks it teaches inform reasoning, they don't predict results.
- The diagram routes described in [pm-visuals](../pm-visuals/SKILL.md) (Mermaid, standalone HTML, an optional external diagramming connector) depend on which tools the host actually exposes at runtime; this plugin doesn't bundle or guarantee any particular connector.
- Cross-host behavior (Claude Code skill invocation vs. Codex vs. other MCP-compatible hosts via the generic skills installer) has not been exercised end-to-end in this verification pass — only the plugin's own files and scripts were checked directly.
- Source URLs cited in `references/sources.md` were checked to resolve to the correct organization/author's page at the time of writing; they are not monitored for future link rot.

## Reproducing these checks
```bash
python3 -m unittest scripts/tests/test_discovery_digest.py -v
python3 scripts/metrics_lookup.py activation
python3 -c "import json; print(len(json.load(open('skills/pm-objectives/references/metrics-catalog.json'))))"
```
