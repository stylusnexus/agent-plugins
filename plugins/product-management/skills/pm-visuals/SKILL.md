---
name: pm-visuals
description: "This skill should be used when product management work needs diagrams and analysis: strategy canvases, value curves, double-diamond discovery, capability maps, activity systems, roadmaps, Five Forces, PESTEL, or SWOT."
---

# Product Diagrams and Analysis

Read [shared principles](../product-manager/references/principles.md). Produce an actual diagram together with decision-relevant analysis when a visual is requested or materially clarifies the work. A prose description of a diagram is not a delivered diagram.

## Analysis-to-visual contract
1. Identify the decision, audience, scope, date, and relevant PM workflow. Establish the substantive analysis with `pm-canvas`, `pm-value-proposition`, `pm-discovery`, `pm-capabilities`, `pm-strategy-fit`, `pm-roadmap`, `pm-market-analysis`, `pm-teams`, or `pm-strategy` before selecting a visual form. Iterate as the visual exposes gaps.
2. Create a small underlying table of nodes, factors, values, relationships, horizons, or statements. Assign stable IDs and evidence references. Separate observed evidence, inference, hypothesis, accepted choice, proposed target, and unknown. Accepted choices are not proven outcomes. Label fictional examples prominently.
3. Preserve those distinctions in the diagram using text and shape/line patterns as well as color. Do not convert unknowns to zero, connect lines across missing observations, imply causal proof with an unsupported arrow, invent numeric scales, or present proposed dates as commitments. Add legends, units, scope, source/date, and scoring anchors where relevant.
4. Deliver a companion accessible table and concise analysis: what the diagram shows, the strongest support, consequential gaps or tensions, and the decision/test it suggests. Reference the same IDs in visual, table, and analysis; correct contradictions before delivery.
5. Validate labels, counts, plotted positions, hierarchy, missing data, attribution, and legibility. Inspect the rendered result when tools permit. State accurately which artifacts were created and what was checked; a structural HTML check is not a visual inspection.

## Choose the artifact
- **Default to Mermaid** for static relationships, capability hierarchies, activity systems, and decision flows when the host renders it — it needs no external connector and stays fully text-portable. Label relationship types; provide a table fallback. Do not depend on a remote Mermaid CDN in an offline artifact.
- **Lucid is an optional connector**, not a default. Read [Lucid and Mermaid routing](references/lucid-mermaid.md) for when it's worth using instead — mainly editable workshop boards a static diagram can't represent. Inspect live tool capabilities before relying on it, and never assume it exists on a given host. Do not silently drop a diagram type the user specifically asked for because the preferred tool isn't available — fall back and say so.
- Use editable standalone HTML with inline SVG/CSS for canvases, plotted curves, discovery diagrams, or multi-panel reports. Keep essential content usable without scripts or network access. Include semantic headings, SVG titles/descriptions, accessible data tables, readable contrast, and print styles. Editable source does not imply a drag-and-drop editor.
- For an in-chat interaction that helps the decision, read the host's `visualize:visualize` skill if available. Keep interactive in-chat output distinct from standalone files. Do not assume that capability exists on every host.
- For requested PDF, spreadsheet, document, or slide exports, read the appropriate available export skill/tool and generate that format. Browser print support alone does not mean a PDF was made; HTML is not PPTX. Retain editable source and report export limitations honestly.

## Match the diagram to the analysis

| Diagram | Required visual | Required analysis |
|---|---|---|
| Product Strategy Canvas | Five labeled sections from Roger Martin and A.G. Lafley's *Playing to Win* choice cascade — Winning Aspiration, Where to Play, How to Win, Capabilities, Management Systems — plus a Key Measures & Open Assumptions section | Explain reinforcing choices, trade-offs, assumptions, and decisions; show who could copy this and why they wouldn't. Distinguish this from a value curve. |
| Value curve | Factors on horizontal axis; explicitly anchored offering level vertically; current alternatives as observed series; proposed targets visibly distinct; breaks at unknowns | Define segment, factor relevance, rating method, evidence, and what divergence sacrifices or improves. Never claim the highest total is the best strategy. |
| Double Diamond discovery | Discover/Define (problem space) and Develop/Deliver (solution space) as two divergent/convergent diamonds; uncertainty and iteration visible | Link research to problem framing, then competing solutions and tests. Show evidence/decision gates; diamonds do not mandate a waterfall or prove validation. |
| Opportunity solution tree | Outcome root; opportunity, solution, and assumption-test layers below it as parent/child nodes | Explain which opportunities are evidenced, which solutions are being tested, and what would change priority. An unaddressed branch is not a validated one. |
| Capability map | Defined L1/L2 abilities nested or linked; current and target states differentiated | Explain boundaries, strategic importance, evidence/maturity unknowns, dependency gaps, and roadmap implications; do not draw an org chart or software inventory. |
| Strategy-fit activity system | Strategic choices and activities with labeled reinforcing/conflicting/unknown links | Explain mechanisms and counterarguments, distinguish consistency from reinforcement, and connect imitation incentives/barriers to assumptions. Coherence does not prove demand. |
| Outcome roadmap | Now/Next/Later lanes with objective/outcome IDs, discovery or delivery state, dependency links where useful | Explain sequencing, confidence, acceptance/revisit criteria, and known commitments. Avoid replacing feature names with vague benefit words. |
| Strategic context | Vision/why → strategy/how and where-to-play/how-to-win → objectives/what outcomes → roadmap/sequence, with a learning return loop | Explain the significant customer/company problem, measures of success, links between choices and objectives, and evidence that could change the strategy. |
| Five Forces | Rivalry centered among entrants, substitutes, supplier power, and buyer power | State industry boundary and each force's mechanism/evidence, uncertainty, implications for attractiveness, and choices. Do not infer force strength from the number of firms alone. |
| PESTEL | Six labeled panels for Political, Economic, Social, Technological, Environmental, Legal | For each material external signal give source/date, exposure mechanism, horizon, impact direction, uncertainty, and response. Verify live legal/regulatory facts; omit unsupported claims. |
| SWOT | Strengths/Weaknesses internal; Opportunities/Threats external in a labeled 2×2 | Support each item and convert consequential combinations into choices/tests. A wish is not a strength; a feature idea alone is not an external opportunity. |

## Reuse without copying conclusions
Read [templates](references/templates.md) for input contracts and reusable layouts. Open [offline gallery](examples/diagram-gallery.html) as a worked visual example. Every example is fictional; replace data and evidence before project use. Do not merely link the gallery as if it were the user's finished analysis. Generate the requested project-specific artifact and link it.

For narrow work create only the useful view. For larger work keep stable IDs across strategy, capability gaps, objectives, discovery tests, and roadmap bets so the user can follow the reasoning. Do not build a generic rendering framework to satisfy a one-off diagram request.

## Artifact creation and human review
Read the [artifact and redline workflow](../product-manager/references/artifacts.md) when creating, rendering, editing, or reviewing deliverables, including browser inspection requirements. For standalone HTML beyond the diagrams covered here, or an editorial redline pass on wording, use the host's `html`/`redline` skills, or the `html`/`redline` skills from the `reporting-comms` plugin when installed.

## Kano model
Use the [Kano workflow](../pm-discovery/references/kano.md) when assessing expected basics, performance attributes and delighters. It covers paired questions, response classification, mixed findings, conceptual diagrams and strategy-aware prioritization. Do not infer survey findings from team opinion.

## Journey maps
Use the [guided journey workflow](../pm-discovery/references/journey-mapping.md) for evidence-linked lanes, variants, Lucid setup, Mermaid fallback, browser checks and redline feedback. Do not fabricate numeric emotions to satisfy chart syntax.
