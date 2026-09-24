# Lucid and Mermaid

## Default: Mermaid
Mermaid is the default for diagrams in this plugin. It's plain text, needs no external connector, and renders anywhere the host supports it. Use it for the static relationship diagrams — capability hierarchies, activity systems, decision flows — referenced elsewhere in `pm-visuals`.

## Optional: Lucid connector
Some hosts have a Lucid connector configured (Lucidchart for structured diagrams, Lucidspark for workshop boards). When one is available and the request calls for an editable cloud diagram, or a workshop-board layout Mermaid can't represent (multi-panel boards, sticky notes, dot voting), use it for that request instead of Mermaid. Never assume the connector exists on a given host, and don't silently substitute a static Mermaid diagram when the user specifically asked for an editable board.

1. Read the relevant PM analysis, and any document already being edited, before touching the connector. Keep evidence IDs and unknowns visible in whatever gets produced.
2. If a Mermaid diagram already exists, bring it in through the connector's Mermaid-import path rather than re-authoring it by hand; use dedicated sequence/ERD tools where the connector offers them.
3. For a custom board, read the connector's diagram-specification resource before constructing one, every time the tooling requires it — never guess shape classes or JSON. Validate before treating the board as finished, and resolve any reported errors.
4. Create or update only what was requested; preserve unrelated content already on the board. Return the actual document link. Don't create sharing links, change access, invite people, or post comments unless asked.
5. After creating or editing, read the result back and check section count, labels, note placement, and that evidence/status labels survived the export — a successful API call is not a visual-quality check. Keep a local copy of the underlying data table so the analysis stays portable even if the cloud document later becomes unavailable.
6. If the connector is absent, unauthorized, or fails, say so plainly and deliver Mermaid — or offline HTML/SVG for layouts Mermaid can't express — plus the evidence table instead. State clearly whether a diagram was actually rendered or only produced as source.

## PESTLE/PESTEL workshop board
Lay the six categories out as two rows of three: Political / Economic / Social on the first row, Technological / Legal / Environmental on the second (PESTLE and PESTEL cover the same six categories, ordered differently by acronym only). Give each category a labeled container with discrete, addable notes; add an optional dot-voting legend only if the tool supports it. Size the board to the actual content rather than inventing notes to fill space.

Each note needs an ID, one external signal, an evidence status, and a short implication; keep source/date, geography, horizon, exposure mechanism, uncertainty, and proposed response in a companion table keyed by that ID. Any placeholder note must say it's a prompt, not a finding.

Facilitate in order: set scope, collect ideas independently where feasible, clarify and deduplicate, separate evidence from assumption, discuss implications, optionally vote on what deserves investigation, then assign actions/owners/review triggers. Voting records what participants prioritized — not probability, impact, or validated demand. Never fabricate participants or votes, and keep minority views visible in the record.

Read [Kano guidance](../../pm-discovery/references/kano.md) and [templates](templates.md) for the other diagrams this routing serves.
