# Guided journey mapping: evidence to action

Informed by Paweł Huryn, User Journey Mapping 101, August 26, 2023. Source originals are not included; use the bundled guidance and Markdown worksheets.

## Work through the map together
1. Choose the decision, actor/segment, scenario, goal, start/end boundaries and current or proposed future state. Draft from known context; ask one consequential missing question. Keep different actors or materially different scenarios separate.
2. Gather episode interviews, observation and relevant analytics. With no research, create a clearly labelled hypothesis map and a research plan. Never invent quotes, thoughts, feelings or journey timing.
3. Draft phases and detailed steps together. Include off-product actions, waiting, handoffs, variations and error/recovery paths when material. Keep sequence clear without forcing every person into one happy path.
4. For each step record actions/touchpoints, reported or inferred thoughts, named emotions with context, time if known and evidence IDs. Mixed emotions can coexist. Analytics cannot reveal emotion by itself. Unknown is a valid entry; neither positive nor negative emotion is mandatory.
5. Separate observation, interpretation, customer need/opportunity and solution idea. The source labels some solution ideas “insights”; use explicit columns so suggestions do not masquerade as research findings.
6. Link consequential problems to strategy/objectives, compare alternatives and design tests. A future-state map describes a proposal, not proven improvement. Record owner, next action or a reason to defer; not every mapped issue should be built.

## Lucid setup and output
Read pm-visuals/references/lucid-mermaid.md and live connector instructions. Prefer Lucid for editable maps: phases as columns and actions, thoughts, emotions, evidence, needs and proposed responses as lanes. Include a header for actor/scenario/goal/state/date and stable step IDs. Use branch pages or explicit alternate paths where one grid becomes unreadable. Do not create a cloud document just to configure the suite.

If a user requests an actual map, reuse existing Mermaid verbatim through the appropriate Lucid converter when required by its tool. For a custom grid with no existing Mermaid/SVG, read the Lucid specification resource and validate the specification before creation. Inspect the returned document/export; preserve local data/source and returned link metadata.

Mermaid fallback: use a flowchart for phases and branches plus the evidence table. Avoid Mermaid journey scores unless real, defined ratings exist; the numeric syntax is not a reason to invent emotion scores. For exact lanes offline, use accessible HTML/SVG. Tell the user which format was actually generated.

## Browser and redline review
Render and inspect labels, row/column alignment, branches, text clipping, keyboard readability and source/assumption distinctions. Use the host browser tool. Preserve an accessible table and source file. Follow the chief artifact workflow to generate a local redline page: edit/comment for static narrative or tables; comment-only for scripted visuals. Returned human wording is applied verbatim to the source, with stale anchors surfaced. If Lucid comments are requested, use them within explicit authorization; do not invite collaborators or post comments automatically.

Use the [journey worksheet](../templates/journey-map.md) as the source contract. Deliver the actual project map, evidence table, key decisions and next experiment when requested; a link to a blank template alone does not fulfill that request.
