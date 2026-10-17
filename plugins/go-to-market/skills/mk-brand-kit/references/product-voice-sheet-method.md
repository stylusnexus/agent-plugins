# Product voice sheet method

Most small teams have a general house style (banned phrases, a company-wide tone) but nothing that says how any one product's own voice differs from another product's, or from a founder's personal writing voice. A backend library's error message, a consumer app's onboarding copy, and a founder's personal blog post shouldn't necessarily sound identical — but without a document to check against, that distinction only ever exists as ad hoc judgment. This method closes that gap for one product at a time.

## How to draft it

1. **Read what already exists.** Any house style guide for the company-wide floor (plain, direct, evidence-first tone; a banned-phrase list; any compliance guardrails that bind everything). Then read the actual copy that already exists for the product in question — README, landing page drafts, in-app strings, error messages, changelog entries.
2. **Pull the do/don't word lists from evidence, not invention.** A "don't" word is one that's already crept into existing drafts and clashes with the house floor, or is off-tone for this specific product. A "do" word is one that's already working — pulled from copy an owner has approved, or from language the target audience uses themselves (from `mk-audience`'s evidence, where available).
3. **Write 3–5 before/after rewrites**, each a real or realistic sentence for this product: the generic/off-voice version next to the on-voice version, with a one-line note on what changed and why. Don't invent a "voice" from adjectives (playful, bold, friendly) — show it in actual rewritten sentences.
4. **Check against the house floor**, not instead of it: does every "do" example still pass basic quality checks (could this have been written for any company? is every factual claim supported? does the reader know what to do next?). A product voice sheet narrows the house voice for one product; it never contradicts it.
5. **Mark the whole sheet `HUMAN DECISION REQUIRED`** until an owner reviews and approves it. This is a draft proposal built from evidence, not a ratified standard.
6. **Never overwrite the house style file directly.** Save the product voice sheet as its own artifact (see the [template](../templates/product-voice-sheet.md)) and, once approved, link it from the product's own docs rather than merging it into the shared house file.

## What "evidence" means here

Real existing copy, the house style file's own examples, and (where `mk-audience` has run) real phrases the target audience uses. Not a personality brainstorm, and not a competitor's voice guide — a competitor's tone tells you nothing true about how this product should sound.

A worked example applying this method lives in the [product voice sheet](../templates/product-voice-sheet.md) template, not here — this reference file doesn't carry invented examples, only the method.

This method is original synthesis for a small team's own gap; it draws on no single external source.
