# Customer journey maps

A journey map is a visualization of what a specific actor goes through to accomplish a specific goal — Nielsen Norman Group's definition is worth keeping close, because "actor" and "goal" are both singular on purpose. ([Sarah Gibbons, NN/g, "Journey Mapping 101,"](https://www.nngroup.com/articles/journey-mapping-101/) 2018-12-09.) NN/g's five components — actor, scenario and expectations, journey phases, actions/mindsets/emotions, and opportunities — map directly onto the columns in the [journey map worksheet](../templates/journey-map.md) in this skill.

## Why a journey map is two maps overlaid

Jim Kalbach's term for this whole family of diagrams is **alignment diagrams**: a technique for bringing a customer's experience and an organization's own process into the same view. His framing is precise about what the overlay is for: "by aligning the user's experiences with the business offers, the diagram identifies and highlights the intersections where value can be located." ([Jim Kalbach, "Locating Value with Alignment Diagrams,"](https://experiencinginformation.com/2011/04/19/locating-value-with-alignment-diagrams/) 2011-04-19.) A journey map that only records what the actor does, with no visible link to what the organization is doing (or failing to do) at each step, is half the diagram — it can describe the experience but can't point at where the organization should act.

That's the reason the worksheet carries a **need or problem** and a **proposed response / test** column next to every step, not just the actor's actions and feelings: each row is one alignment point, actor-side and organization-side together.

## Building one

1. **Fix the actor, scenario, and boundary before drawing anything.** One persona, one episode, one clear start and end. A map covering every user type or every path becomes an org chart with feelings attached, and NN/g's observation about siloed metrics applies here too: nobody owns the whole experience unless the map forces the question.
2. **Populate steps from evidence, not assumption.** Each row's *thought/emotion* cell is marked reported, inferred, or unknown — don't default emotional content to whatever makes a tidy narrative arc. An "unknown" cell is more honest than an invented one, and it's a visible flag for what discovery should go find next.
3. **State the map's evidence basis up front.** The worksheet's header line — observed current state, hypothesis, or proposed future state — changes how the map should be read. A proposed-future-state map is a design artifact, not a finding; label it that way so nobody treats it as evidence the future state already works.
4. **Record what the map is for.** "Decision this supports" isn't decoration — a journey map built to find where support tickets originate looks different from one built to design a future onboarding flow, even for the same actor and scenario.
5. **Add a variant lane where the path actually forks.** The worksheet's "Variants / failure and recovery paths" row exists because a single happy-path lane is a simplification — a step where users commonly retry, abandon, or reach support is worth its own lane, backed by the same evidence rule as every other step, not added because the template has room for it.

## Diagramming

Use `pm-visuals`: Mermaid by default, one lane per variant; Lucid when the map needs to become an editable workshop board rather than a static artifact. Don't fabricate numeric values (satisfaction scores, time-on-task) to make a chart render cleanly — unknown stays unknown in the visual, same as in the table. `pm-visuals` handles the browser-check and redline pass afterward through its own [artifact and redline workflow](../../product-manager/references/artifacts.md); this file only owns what goes into the map.

## What the map is for once it's done

Read each row's *proposed response / test* against [product risk](product-risks.md): a proposed response is a hypothesis about what would improve the step, and it carries the same evidence-status obligation as anything else in this suite — **evidence-backed**, **hypothesis**, or **accepted** ([shared principles](../../product-manager/references/principles.md)). A finished map with no proposed responses attached is a description, not yet a decision aid.
