---
name: mk-copy
description: "This skill should be used when the user asks to write or edit a landing page, a README, a store listing, an app description, an announcement, a press release or announcement blurb, launch copy, or any copy meant to reach an audience."
---

Copy meant for an outside reader: a landing page, a README opener, a store listing, an app description, a launch or press blurb. The job is the same across formats — get a stranger from "what is this" to "I want it" as fast as honesty allows, in writing that still makes sense if only one paragraph of it is ever seen.

## When to use this skill

Any copy that will reach someone outside the team: a hosted landing page, a README's opening section, a store or marketplace listing, an app description, an announcement or press blurb, or launch-day copy. Not internal docs, and not the underlying value proposition or story itself — those come from `mk-positioning` and `mk-founder-content` before this skill drafts a word.

## Workflow

1. **Bring the real inputs, don't invent them.** Confirm the value proposition and the objection this copy needs to answer already exist (`mk-positioning`, `mk-audience`). Writing copy before those exist means guessing at what a stranger needs to hear. Hard rule for the draft itself: never invent a product capability, a feature, a person's stated reason, a result, or "we've talked to X" evidence — check every sentence against a supplied fact (claim → source) and write anything unsourced as `MISSING INFORMATION`, not as a described fact. One customer's result isn't "most customers"; a self-reported result gets labeled as self-reported, not as a verified outcome (see `marketing-lead/references/principles.md`).
2. **Structure the page.** For a landing page, follow [the landing-page copy formula](references/landing-page-formula.md) — headline in two passes (plain value, then one hook), a page order adapted from Julian Shapiro's public guidance, and features each paired with a real objection. Start from the [landing-page skeleton](templates/landing-page-skeleton.md). Treat a README's opening with the same discipline — it's often the first and only thing a visitor reads before deciding whether to use a project (this suite's own reasoning) — using the [README opening skeleton](templates/readme-opening-skeleton.md).
3. **Write every section so it survives being lifted out.** A search result, an AI assistant, or a forwarded message shows one section with no other context. Apply [extractable-section writing](references/extractable-writing.md): a real subject and verb to open, the claim before the caveats, jargon defined on first use in *that* section, one idea per section.
4. **Add a real story only if one exists.** A true before/after earns a claim faster than an assertion does. Find and structure it per [story structure in copy](references/story-structure-ai-drafting.md), which points to `mk-founder-content`'s story-finding method rather than duplicating it — fact-check every beat, and route it through the byline rule (a personal story runs only under the approval of the person it happened to).
5. **Persuade honestly or not at all.** Run every lever — scarcity, social proof, authority, reciprocity, commitment — through the [honest-persuasion filter](references/persuasion-levers-honest.md): usable only when the fact behind it is true and checkable, right now, for this product.
6. **Check it against the public bars before it ships.** The [pre-publish content check](references/pre-publish-content-checklist.md) pulls from plain-language, accessibility, and truth-in-advertising guidance that already exists publicly — plain-language readability, WCAG basics (alt text, descriptive links, no meaning by color alone), and FTC endorsement-honesty rules. Nothing ships without a claim → source row for every fact in it.

## Routing to sibling skills

- `mk-positioning` — for the value proposition and category claim this copy has to carry; get this settled first.
- `mk-audience` — for the real objection and the audience's own language, not an imagined one.
- `mk-founder-content` — for finding and structuring a true story before it becomes a copy section.
- `mk-search` — once the copy exists, to make the same sections citable and findable.
- `mk-brand-kit` — for the product's own voice, once a voice sheet exists, so this copy doesn't drift from it.
- `marketing-lead` — for where this piece of copy fits the team's broader, hours-bounded plan.

## Outputs

A draft of the requested copy (landing page, README opener, listing, or announcement), a claim → source table for every factual statement in it, and any gap labeled `MISSING INFORMATION` rather than invented. Alongside the draft, a short note naming which persuasion levers from [the honest-persuasion filter](references/persuasion-levers-honest.md) were used and why each is true and checkable right now, plus any lever deliberately left out and why (usually because the fact behind it isn't real yet). Drafting is not publishing — see `marketing-lead/references/principles.md`: plans and drafts are not permission to post them.

## Adaptable prompt

"Draft [format — landing page / README opener / store listing / launch blurb] copy for [product], for [specific audience]. Lead with [the one real objection or proof point to answer]. Use only facts I give you or that you fetch and cite; flag anything you can't source instead of guessing."
