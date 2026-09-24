# Landing-page skeleton

Fill-in form derived from [the landing-page copy formula](../references/landing-page-formula.md) and [extractable-section writing](../references/extractable-writing.md). Delete every instruction line (in *italics*) once its field is filled. Every real fact, name, and number must come from the actual product and real user answers — nothing here licenses inventing one.

## Headline

- **Pass 1 — plain value proposition:** *State the problem without the product against the better outcome with it, as one concrete action statement. A stranger who reads only this line should know exactly what the product does.*
  →
- **Pass 2 — with one hook:** *Add a single bold, specific claim, or preempt the one biggest objection. Don't try to answer every objection here.*
  →

## The trade-off check

*Before shipping any line below, ask: does it make the reader want the outcome more, or does it remove a reason to hesitate? If it does neither, cut it.*

## Page sections, in order

1. **Identity/nav** — *logo, minimal links.*
2. **Hero** — headline (above) + one supporting line + primary image or product shot.
3. **Proof** — *real testimonials, real numbers, real logos only. Omit this section entirely if there's no real proof yet — do not fill it with a placeholder that looks real.*
4. **First call to action.**
5. **Features, each paired with the real objection it answers** — see table below.
6. **Repeat call to action.**
7. **Footer.**

## Finding the real objection

*Ask actual users or people who almost bought and didn't: what nearly stopped them. Don't invent this from imagination — pull it from `mk-audience`'s evidence if it already exists.*

Real objection heard: →
Who said it / where it came from: →

## Feature / objection pairs

| Feature (real) | Objection it answers (real, heard from someone) | One line answering it |
|---|---|---|
| | | |
| | | |
| | | |

## For a technical or developer audience

*Replace adjectives with demonstration — a real screenshot, real code, real output. The biggest unstated objection is usually "how much friction before I see this work."*

Runnable example or real output to show: →

## Claim → source table

*Every factual claim on the page needs a row here before it ships — see the [pre-publish content check](../references/pre-publish-content-checklist.md).*

| Claim | Source |
|---|---|
| | |

---

### Example (fictional)

*Illustrative only — a made-up product, not a real one, with no real-world numbers.*

- **Product:** a small open-source CLI that catches broken links before a docs site deploys.
- **Pass 1 headline:** "Find broken links in your docs before they ship."
- **Pass 2 headline:** "culvert scans your build output, not your source files — so it catches links your editor can't see."
- **Feature/objection pair:** Feature — checks rendered HTML, not markdown source. Objection — "doesn't my linter already do this?" Answer — a markdown linter checks syntax; this checks the actual rendered links after templating and redirects run.
