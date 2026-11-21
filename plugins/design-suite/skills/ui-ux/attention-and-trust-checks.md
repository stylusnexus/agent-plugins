# Attention and trust checks (conversion without manipulation)

Use this to check whether a page or flow helps people act with confidence, without tricks. These are expert-review checks, not user research. Thresholds are recommended defaults unless marked as a cited figure from the source; none is a standard. Tag findings VERIFIED, NEEDS-TEST or MISSING INFORMATION. Report only; do not change or launch anything unasked. For consent and data checks, see `ethics-and-consent-review.md`.

## 1. Quick tests (run with real people, or mark NEEDS-TEST)

| Test | How | Pass signal |
|---|---|---|
| Five-second test | Show the page for five seconds, then ask "What does this offer?" and "Is it for people like me?" | Most testers answer both correctly (recommended) |
| First-click test | Give a key task, record where the first click lands | Most testers click the right target. Published first-click studies report roughly 87% task success after a correct first click against 46% after a wrong one; treat the figures as an illustration |
| Distinct choices | Show two similar options and ask what separates them | A tester states the difference in five seconds |

Without people, say "not run" and list the test; do not simulate results.

## 2. Attention budget per first screen

1. List every element above the fold (headline, image, nav, offers, links, banners).
2. Give each a share of 100 points for how much attention it pulls (size, contrast, position, motion).
3. The primary action should hold the largest single share, clearly above any policy link or secondary offer.
4. For each element record all three answers: can it go, can it be hidden deeper (tab, later page), can it be smaller or lower? An element with no recorded answer is a finding.

Check: does the primary action visibly win, and does every element have its three answers? Scores are reviewer judgement; say so.

## 3. One question per action

- Each CTA answers one easy question the user asks themselves, stated as their gain ("Get my free sample", not "Submit"). Check: does the label name the benefit in under eight words (recommended)?
- Give each CTA one role (grab attention, build relationship, reassure, encourage action, spread the word) and a stage where the user is ready. Check: a newsletter overlay on arrival has the wrong stage for most visitors.
- Name the fear beside each action: privacy, spam, hidden cost, wasted time, can't undo. Check: is the reassurance visible next to the control without scrolling or hunting?
- Reversal is easy: cancelling or unsubscribing takes no more steps than joining (see the ethics review for counts).

## 4. Redesign shock

When an existing layout changes:

1. List every moved, renamed or removed element.
2. Give each a "what moved" cue: a short notice, a label on the new spot, or a redirect.
3. Check that returning users can still find the top five tasks; mark NEEDS-TEST until tried.

## 5. Pre-launch quality sweep

Check: no typos in headings or buttons; every link resolves; no console errors on key pages; forms accept common formats (postcode case and spacing, phone with spaces) and show the first error at the field on submit; error and success states exist. Each failure is VERIFIED only if reproduced; list pages and browsers not covered.

## 6. Trust through real people

- Every person shown has a name and real role; photos are of actual staff or customers.
- Testimonials are unscripted where possible; keep some critical reviews and show review counts.
- Check: does any quote, logo or number lack a source? Mark it a placeholder or remove it. Never present invented evidence as real.

## 7. Metrics with counter-metrics

| Item | Check |
|---|---|
| Each goal has a target, an owner and a counter-metric | Lead volume paired with lead quality; sign-ups paired with cancellations |
| Three areas tracked together | Conversion, usability and engagement; at least one of each in the review |
| Task numbers per CTA | At least one of time on task, failure rate, direct-route completion or errors covers every main CTA |
| Usability score recorded per release | System Usability Scale (ten statements, 1 to 5, scored out of 100). Cited figures: average about 68; below 50 means fix usability first |

Check: does the record show last release's score, and who owns the counter-metric?

## Output

Use the table in `heuristics-review.md` and add an evidence tag. Close with tests not run (five-second, first-click, SUS survey), data not supplied, and the owner decisions needed. A rising conversion number is not proof of a good design; ask what the counter-metric did.
