---
name: pm-canvas
description: "Use when the user asks to build, fill in, teach, review, or update a one-page product strategy canvas covering winning aspiration, where to play, how to win, capabilities, and management systems."
---

# Product Strategy Canvas

Read [shared principles](../product-manager/references/principles.md) first.

## What this is
A one-page synthesis, not a substitute for the deeper work in `pm-vision`, `pm-strategy`, `pm-value-proposition`, `pm-objectives`, `pm-capabilities`, `pm-strategy-fit`, and `pm-discovery`. It follows Roger Martin and A.G. Lafley's *Playing to Win* strategy choice cascade — five integrated choices (winning aspiration, where to play, how to win, capabilities, management systems) — plus a measures-and-assumptions section this plugin adds to connect the cascade to the rest of the workflow. The [template](templates/product-strategy-canvas.md) carries the full public grounding and attribution for each choice.

Keep this distinct from a Blue Ocean-style value curve (which plots competing offerings against ranked factors — that work lives in `pm-value-proposition`) and from Strategyzer's Value Proposition Canvas or Business Model Canvas, which [sources](../product-manager/references/sources.md) names as further reading but this plugin does not reproduce.

## Filling it in
1. Confirm product, owner/audience, date, and status (draft vs. accepted — accepted means committed, not proven). Default to co-drafting: explain a box, propose a draft from real evidence, let the user decide. Skip the explanation when the user wants a fast draft or a straight review instead.
2. Fill only what the evidence supports; leave the rest open. Tag every entry evidence-backed, a hypothesis, or an accepted choice.
3. Work the choices in whatever order surfaces the live decision — the cascade does not have to be filled top to bottom, but each choice should be checked against the others once drafted. Each row below names the skill this plugin uses internally; when telling the user what's next, describe the actual work (e.g. "let's pressure-test whether this is defensible"), not the skill's file name. Move anything unsettled into:
   - Winning aspiration → `pm-vision` for the underlying mission/vision work
   - Where to play and how to win → `pm-strategy`
   - The customer-value reasoning behind how to win → `pm-value-proposition`
   - Capabilities → `pm-capabilities` for a full current-vs-target capability map
   - The metrics inside management systems → `pm-objectives` for real metric definitions (baseline, target, owner, cadence)
   - Open assumptions → `pm-discovery` for the cheapest test of each
   - Whether the five choices actually hold together → `pm-strategy-fit`
4. Before calling it done, run the fit checks in the template: who could copy this and why wouldn't they; do the choices reinforce each other or quietly fight (check each pair, not just at a glance); what has to be true, and what's the cheapest test of that; and name the main strategic fork out loud — the single biggest either/or this canvas has actually committed to. Flag any competitor fact used in "how to win" (a price, a feature, whether a named product still exists) that hasn't been verified today, rather than stating it as current. A filled canvas is a compressed hypothesis set, not a validated strategy.
5. When asked, connect accepted choices to objectives and an outcome roadmap; keep execution detail out of the canvas itself.
6. Deliver the populated canvas with its evidence/assumption trail and open decisions. Use the Markdown template by default — it needs no special tooling. If the user wants a slide or board version, carry the framework attribution forward, and don't claim a document was produced when only Markdown was.

Read [working with strategy](../product-manager/references/working-with-strategy.md) for running this as a workshop or revisiting it over time.

## Teaching mode
Explain a choice only when it bears on the decision at hand — draft from the user's real situation, name the trade-off, then ask for the call. Teach how the choices constrain each other (why a where-to-play choice narrows what how-to-win can credibly promise; why management systems have to reinforce the specific capabilities chosen, not measure everything) rather than reciting definitions. If you reach for a published company's strategy as an example, label it a historical illustration, not a current account of their strategy — the framework's own sources are explicit that named-company examples describe the moment they were written, not the present.

Use the working-through order below when someone wants to learn the cascade rather than just fill it in:
1. Start with winning aspiration — a vague aspiration makes every later choice arbitrary.
2. Where to play and how to win are a matched pair: a where-to-play choice is only real once it implies specific things the offering must be superior or cheaper at.
3. Capabilities and management systems are where good strategies most often go slack — ask what capability the how-to-win choice actually depends on, and whether anything currently measures or protects it.

## Prompt
"Build a product strategy canvas from what we actually know: winning aspiration, where to play, how to win, capabilities, and management systems. Separate accepted choices from assumptions, and explain how the choices reinforce or constrain each other. Then run the fit checks and name the next decision that needs evidence."

For worked examples and critique patterns, see [strategy teaching and critique](../pm-strategy/references/teaching-examples.md).
