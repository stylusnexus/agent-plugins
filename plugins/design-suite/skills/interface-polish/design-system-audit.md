# Design system audit

Review a design system or component library as one system, not screen by screen. Report-only unless asked to implement. This is expert review of artefacts, not user research. Numbers marked "recommended" are defaults; the system's own documented value wins.

Evidence labels: VERIFIED (counted or observed in the source), NEEDS-TEST (plausible, not run), MISSING INFORMATION (no source given). List "Checks not performed" at the end. Never state that a system complies with anything; report what was found.

## Interface inventory

- Collect every distinct screen or state in scope. Group elements by the job they do (confirm, navigate, filter, warn), not by how they look.
- Check: more than one module per job is a merge candidate. Record the count per job.
- Count variants of one thing: distinct greys, button versions, heading sizes, card styles. Report the number next to the intended count. A large gap is a finding.
- Check: every counted duplicate lists the screens it appears on.

## Naming

- Name by purpose, not appearance. Check: if the style changed tomorrow, the name would still be true ("alert", not "red box").
- A new teammate can guess when to use the pattern from its name alone. Check: ask someone outside the team to place three names on three screens.
- One term across design files, code and copy. Check: grep for each pattern name in all three; mismatches are findings.
- If nobody can name a pattern, its purpose is unclear or it overlaps another. Flag it.

## Merging and variants

- Specificity test: merge two patterns only if a change to one should change the other. Check: write one sentence per pair; if the answer is "not necessarily", keep them apart.
- Each pattern declares its core features and what its variants change. Check: a change to core can be predicted to reach every variant by reading the docs.

## Roles and meaning

- One primary action per screen. Check: count primary-styled actions per view; more than one is a finding.
- Buttons act on the page; links leave it. Check: no button navigates away, no link changes data. Body links stay plain.
- Colour keeps one meaning. Many blues are fine if blue always means the same thing. Check: blue (or any signal colour) never styles non-interactive text.
- Colour proportions are part of the brand. Check: describe the ratio in one sentence ("mostly white, accent in small doses") and compare a new screen against it.

## Base values and steps

- Colour, type, spacing and timing each have one base value and derived steps. Check: count distinct values in use per category against the declared steps (one published audit found 62 greys).
- Motion duration grows with distance travelled and element size. Recommended: a full-screen move gets at most two steps above the base duration. Motion never blocks task completion. Check: complete the main task with animations at their slowest; nothing waits on them.

## Principles and brand

- Three to five principles, ranked for conflicts, each pinned to a real screen, each testable. Check: pick one screen element and name the principle it serves; an element with no stated purpose is a finding.
- Brand traits come with a "not" (for example "playful, not childish"). Recommended: five to seven traits. Check: each trait maps to a visible decision.
- Three to five signature moments (a shape, a motion) repeat across the product. Check: each appears in at least three templates in the same form.

## Exceptions and intake

- Keep an exception log for business one-offs (a promo banner, a partner badge). Check: entries have a date and owner; re-review when entries multiply.
- Intake gate: a pattern joins the library on its second real use, or when it is plainly generic. Check: every library pattern names two real consumers. Undocumented one-offs are logged, not ignored.
- Reuse must pay back: a shared component costs roughly two to three times a one-off (recommended planning figure) and breaks even near the second or third use. Check: no component is forced where a custom fit serves users better.

## Documentation

Minimum per pattern: name, one-to-two-sentence purpose, live example, variants, related patterns, when not to use it. Check: open five random patterns; each has all six.

Content slots: each module lists required and optional slots and their order. Check: put a double-length title in the module; if the main action leaves the view, fix the module, not the copy.

## Governance

- Strict versus loose is stated, with a documented exception route. Check: a team can find where to ask for an exception; strict rules with no stated reason get overridden silently.
- A named owner with allotted time. Check: the owner and weekly hours are written down. A fully shared model usually means two people do the work.
- Start from pain: components trace to a repeated complaint from people who use them. Check: each planned component names the chore it removes and who repeats it.
- Goals carry a number, a baseline and a review date (for example share of pages using the component). Check: all three exist for every goal; MISSING INFORMATION otherwise.
- Hold naming and contribution debates in a scheduled session every four to six weeks (recommended); park them in a list during build work.

Severity follows `review-format.md`.
