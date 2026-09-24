---
name: mk-positioning
description: "This skill should be used when the user asks for positioning, who a product is for and what it beats, why we win, a one-liner, a tagline, a messaging hierarchy, how to describe the product to a stranger, or what category to claim."
---

## Purpose

Positioning decides what market a product is claiming to win, and why, before a single word of copy gets written. It answers: for this buyer, against this alternative, why does this product win — a decision about which fight the product is entering, not a tagline.

## When to use

Use this when someone asks who a product is for, what it replaces, why it wins, what to say to a stranger in one line, what category to claim, or when an existing positioning feels shaky and needs to be re-argued from evidence instead of gut feel. If the actual ask is "write me a tagline" with no settled positioning underneath it, work the positioning first — `mk-copy` turns settled positioning into words; it doesn't invent the positioning.

## Workflow

1. **Name the real competitive alternative.** What would this buyer do if the product didn't exist — a named competitor, an adjacent tool, a spreadsheet, or doing nothing? Getting this wrong makes every later step answer a question nobody's asking. See [dunford-five-components.md](references/dunford-five-components.md).
2. **List differentiated capabilities against that specific alternative.** Actual features, not adjectives any competitor could also claim.
3. **Attach value to each capability.** What concrete outcome does it produce for the buyer? A capability with no value attached is a spec sheet, not positioning.
4. **Pick the narrow segment that cares most about that value** — not everyone who could plausibly use the product. Bring in `mk-audience` if the segment itself isn't settled yet.
5. **Choose the market category** that makes the value obvious to that segment without a long explanation, then check it still matches the alternative from step 1.
6. **Run the stakeholder check before shipping.** What does this positioning do for the customer, for the business, and for the wider community it touches (a competitor named unfairly, a platform's norms)? See [stakeholder-check.md](references/stakeholder-check.md). A claim that only survives scrutiny on one of those axes needs another pass, not a ship.
7. **Fill the [positioning canvas](templates/positioning-canvas.md)** and write the one-liner from it.

Expect to loop rather than run this once top to bottom: a different alternative in step 1 usually changes which capabilities matter in step 2, which can shift the segment in step 4. Record the alternatives and segments considered and rejected at each step — that record is what lets the positioning be revisited later without starting over.

## Routing

- `mk-audience` — when the target segment itself needs research or definition before step 4 can be answered honestly.
- `mk-copy` — once positioning is settled, to turn it into landing-page or README copy.
- `pm-value-proposition` — from the `product-strategy` plugin, if installed, when step 3 stalls because the customer value itself is unclear.
- `marketing-lead` — for the larger plan this positioning feeds into, or to bring the stakeholder check into a bigger decision.

## Outputs

A filled [positioning canvas](templates/positioning-canvas.md) (alternative, differentiated capabilities, value, segment, category, plus the rejected options), a one-line positioning statement, and — where the stakeholder check surfaced an open question — a note on which axis (customer, business, or community) is still unresolved.

## Adaptable prompt

"Here's what [PRODUCT] actually does: [real description]. The people using it today do this instead: [real alternative(s)]. Walk through the five-component method to find the strongest honest positioning, show the alternatives and segments you considered and rejected at each step, then run the stakeholder check before finalizing anything."
