# Two starting points for discovery

Discovery tends to start from one of two places, and naming which one changes what "done" looks like.

## Starting from a rough idea (initial discovery)
For a market or product concept with no committed backlog yet, use the UK Design Council's Double Diamond, first shared publicly in 2004 per the Design Council's own history of the model ("In 2004, Design Council started to share the Double Diamond at conferences and in presentations") and "Launched in 2004" per the Design Council's Framework for Innovation page, which builds the Double Diamond into a wider set of design principles and methods and describes the process as non-linear: "Many of the organisations we support learn something more about the underlying problems which can send them back to the beginning." (<https://www.designcouncil.org.uk/resources/the-double-diamond/>, <https://www.designcouncil.org.uk/resources/the-double-diamond/history-of-the-double-diamond/>, <https://www.designcouncil.org.uk/resources/framework-for-innovation/>). This plugin frames the first diamond as a problem space and the second as a solution space; the Design Council's own words, from team member Anna White on its history page, are "designing the right thing" for the first half and "designing the thing right" for the second:
- **Discover** — widen out to understand the problem rather than assume it: candidate segments, their needs, existing alternatives, real constraints.
- **Define** — narrow to the market worth pursuing and the value hypothesis.
- **Develop** — widen out again to generate distinct concepts, channels, pricing, and positioning, including doing nothing.
- **Deliver** — narrow to a small-scale test of the assumptions that would most change the decision.

Widen before narrowing in each diamond; convergence means picking the best-supported direction, not arriving at the one provably correct answer.

## Starting from an existing product (continuous discovery)
For a strategically meaningful outcome or known problem inside a shipping product, running continuously alongside delivery rather than as a one-time phase, use Teresa Torres's opportunity solution tree from *Continuous Discovery Habits* (2021) (<https://www.producttalk.org/opportunity-solution-trees/>). The tree has four layers:
- **Outcome** — the single desired business result at the root.
- **Opportunities** — the customer needs, pain points, and desires that would drive that outcome if addressed.
- **Solutions** — candidate ways to address a given opportunity.
- **Assumption tests** — how the team will evaluate whether a solution actually creates customer and business value.

The tree stays a living document: branches get added as interviews surface new opportunities, and a branch with no evidence behind it is a legitimate, visibly unaddressed node — not something to prune to make the tree look finished.

## Running discovery and delivery together
Neither track needs every phase or branch resolved before code gets touched — explain the open question, draft a useful next step, and move. The same cross-functional group can staff both at once; the loop only works if release outcomes, analytics, support signal, and interviews keep feeding back into the diamond or the tree rather than dead-ending in a shipped feature. A handoff should record the evidence behind the bet, unresolved risk, how success will be recognized, and what would trigger revisiting it. Avoid treating a "validated" backlog item as certainty, requiring every question closed before delivery starts, or ruling out learning through a small production-code experiment.

## Diagramming
Use `pm-visuals`. Default to Mermaid; Lucid is an optional connector, worth reaching for mainly when the diagram needs to become an editable workshop board. For initial discovery, draw the Double Diamond and label the halves Discover/Define/Develop/Deliver, with this plugin's problem-space/solution-space framing (see above) called out across the two diamonds. For continuous discovery, draw the opportunity solution tree instead of a second diamond pair, and show the learning loop explicitly in either case.

This is one credible reading of two widely taught frameworks, not the only correct one — when teaching it, distinguish the Design Council's structure, Torres's tree, and this suite's own operational advice.
