---
name: pm-canvas
description: "This skill should be used when the user asks to create, fill, teach, review, or update a Product Strategy Canvas, especially the ProductCompass canvas by Pawel Huryn."
---

# Product Strategy Canvas

Honor applicable repository instructions and prefer a project-local version of this skill when present.

Read [shared principles](../product-manager/references/principles.md) before applying this workflow.

## Purpose and attribution
Use Paweł Huryn / The Product Compass's Product Strategy Canvas as a compact synthesis of strategic choices. See the [public source notes](../product-manager/references/sources.md). Use the [adapted Markdown template](templates/product-strategy-canvas.md); preserve its CC BY-SA 4.0 attribution when copying or adapting it.

Do not confuse this canvas with the Blue Ocean Strategy strategy canvas/value curve. The value curve compares offering factors; it is one input to the broader product strategy.

## Workflow
1. Establish product, owner/audience, date, scope, and draft/accepted status. Read current product evidence and accepted strategy. Default to **guided co-working**: explain the current choice, draft a useful section from available context, and help the user decide. Honor explicit **workshop**, **draft**, or **review** requests without unnecessary teaching or approval gates.
2. Read the template and fill only what is supported. Preserve unknowns. Give each material statement an evidence reference, hypothesis label, or accepted-choice label; an accepted choice is not proof its assumptions are true.
3. Work in any useful order; revisit choices together. Do not force the user to answer ten boxes in sequence. Use focused support skills for unsettled parts:
   - Vision, mission, winning aspiration → `pm-vision`.
   - Market segments, relative costs, trade-offs → `pm-strategy`.
   - Value proposition and value curve → `pm-value-proposition`.
   - Key metrics → `pm-objectives`.
   - Growth and sales/marketing channels → `pm-growth`.
   - Capabilities, resources, partners, management systems → `pm-capabilities`.
   - Can't/Won't and Ask Yourself → `pm-strategy-fit` and `pm-discovery`.
4. Keep the ten sections of the source canvas recognizable. Add mission and winning aspiration as optional context when useful to the requested decision; do not falsely attribute a mandatory three-statement convention to Huryn or Martin.
5. Run the three strategy-fit checks: imitation barriers/incentives; reinforcing choices; assumptions and validation. A visually complete canvas is not a validated strategy.
6. Link the chosen strategy to objectives and an outcome-based roadmap when requested. Keep detailed implementation plans outside the canvas.
7. Deliver a compact populated canvas plus evidence/assumptions and open decisions. If the user asks for a visual artifact, use the bundled Markdown template with a suitable document/slide tool and preserve attribution. Default Markdown requires no specialized app. Do not claim a PPTX, Notion page, or chart was generated when only text was produced.

Read [working with strategy](../product-manager/references/working-with-strategy.md) when facilitating a workshop or deciding how to revise the canvas over time.

## Teaching mode
Explain a box when it affects the current decision, show a draft based on the user's product, explain alternatives and trade-offs, then invite the consequential choice. Teach connections between boxes rather than just their definitions. Adapt published examples as historical teaching material, not verified current company strategies.

## Adaptable prompt
“Build a Product Strategy Canvas from our current evidence. Preserve the original sections, distinguish choices from assumptions, and explain the connections. Include mission and winning aspiration where useful. Stress-test imitation, fit, and what must be true, then identify the next strategic decision.”

For guided examples, use [strategy teaching and critique](../pm-strategy/references/teaching-examples.md). Select the canvas by the question rather than product age alone.
