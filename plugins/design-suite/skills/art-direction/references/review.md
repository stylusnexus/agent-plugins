# Review — a fresh pair of eyes on the page

A builder judges its own page badly: it remembers what it meant. The `direction-reviewer` agent sees only the
screenshots and the written sheet, never the code or the builder's reasoning, and says where the page drifted from
the sheet. This file is how to start it, what to hand it and what to do with what it says. It covers
pages only; app screens have no reviewer, and the agent refuses anything but `kind: page`.

## Contents

1. Who runs it and when
2. The packet
3. What is withheld
4. Dispatching it
5. Replying to the findings

## 1. Who runs it and when

The lead runs it, not the builder. The lead is whoever invoked the art-direction run: the caller when the
builder was a delegated agent, or the one session when it did everything (that session dispatches the
reviewer as a fresh agent). The lead builds the packet, dispatches the reviewer and saves what it says;
the builder replies to the findings. The reviewer runs alongside the builder's own look in step 8, not
instead of it.

If this is an app-screen run, stop: there is no reviewer for app screens (#153). The lead builds no packet.

- **Hero checkpoint:** after step 6.2, when the first screen is built and nothing else exists. Drift
  caught here is not copied into ten sections.
- **Finish checkpoint:** after step 8 and before step 9. The motion layer is not built yet, so the
  reviewer lists it as unable to verify (`scenes.mjs` owns it).

Each mode runs once, plus at most one re-review after the builder's fixes. The re-review is the next
folder (`<n+1>`), with `scope: re-review` in its `files.md`, and is scoped to the earlier Blocks findings. A hero verdict of
`fix first` (at least one Blocks finding; otherwise `go`) means fix, then re-review once; a second `fix first` on the hero goes to the user.

## 2. The packet

A folder, `.taste-skill/review/<n>/`, written by the lead. The reviewer's only tool is Read, which cannot list a folder, so the folder carries its own manifest. Nothing in it is written from memory: if a
line is not in `direction.json`, in a screenshot or report the scripts wrote, or in the user's own request, it
does not go in.

| File | Where it comes from |
| --- | --- |
| `files.md` | The manifest, read first. The first line is `kind: page`; then `mode: hero` or `mode: finish`, then `scope: full` or `scope: re-review`, then one line for every other file in the folder (path, viewport, what it shows). "Not shown" means a listed file that is missing or unreadable. It holds no part of the sheet. |
| `packet.md` | The sheet as text, copied from the `direction.json` that `draw.mjs` wrote into its `--out` folder: direction id and one-line rationale; section order with each section's composition; type roles and sizes; palette as proportions; component rules for buttons, nav and footer; the `--have` assets. Then the number of redraws and which slots, and whether `--keep palette,type` was used. |
| `claim.md` | The user's request verbatim, then the sheet's rationale line. The reviewer reads it after it has written its five-second read of the screenshots and before `packet.md`. |
| `laws.md` | The "Laws of the craft" section of `SKILL.md`, copied word for word, so the reviewer can cite a law it cannot look up. Fixed text, not the lead's memory. |
| screenshots | Copied from `.taste-skill/inspect/`, which `inspect.mjs` writes: `desktop-fold.jpg`, `tablet-fold.jpg`, `mobile-fold.jpg` and the full-page sheets `desktop-page-NN.jpg`, `tablet-page-NN.jpg`, `mobile-page-NN.jpg`. Add scene frames only when the sheet deals scroll scenes. |
| old-page screenshots | Redesigns only: the before shots at 1440 and 390, copied from the before folder named in the redesign steps with a `before-` prefix, because that folder reuses the new shots' names. |
| `report.json` | Redesigns only: the `.taste-skill/kept/report.json` that `keep.mjs` wrote. Its `dropped` list is the declared drops, so the reviewer does not flag them. Run `keep.mjs check`, with the owner's drops declared, before building the finish packet; if it has not run, leave `report.json` out and list it in `files.md` as not shown. |
| `earlier-findings.md` | Finish mode, and any re-review: the hero review's `findings.md`, copied in so a fix cannot quietly regress. On a re-review the reviewer checks only whether the earlier Blocks findings are fixed, reports any new Blocks, and adds no new taste notes. |

**Hero mode** takes its shots by running `inspect.mjs` on the half-built page and copying only the three
`-fold.jpg` files. The page is not finished, so its WARN and FAIL lines mean nothing yet.

## 3. What is withheld

The reviewer must not see: source and CSS, the builder's critique and its scores, the builder's reasons for any redraw, the
per-section claims the builder wrote in step 2, and the inspector's WARN and FAIL list, so the review is
not anchored on the meter or on the builder's intent. The lead adds no notes, hints or
"known issues" to the packet.

## 4. Dispatching it

Start a fresh agent with an empty context (the `direction-reviewer` agent) and tell it only two things:
the review folder path and the mode, hero or finish. The lead does not paste the sheet, the screenshots or the builder's
thoughts into the prompt; it reads `files.md` first and then the folder.

The reviewer cannot write files. The lead saves its reply as `.taste-skill/review/<n>/findings.md`.

It returns one ranked "Do next" list of at most 7 items (plus a `go` or `fix first` verdict in hero mode),
per-slot verdicts of match, partial or miss, what it is unable to verify, and on redesigns what the old
page did better. Each finding has a severity: Blocks (it contradicts a stated sheet slot), Weakens (it
breaches a named law), or a taste note, which can never block.

## 5. Replying to the findings

The builder writes `.taste-skill/review/<n>/replies.md`: one line per finding, in the finding's id order, each either

- `fixed` naming the screenshot that now shows it, or
- `disputed` quoting a sheet line that contradicts the finding.

A finding that contradicts a sheet slot (Blocks) cannot be disputed; fix it. Disputes are for law breaches
and taste notes only. An unanswered finding blocks the report: step 10 lists every finding with its reply,
and the lead reads `replies.md` before reporting. This extends the rule in step 7: the builder does not argue with the
meter, and does not argue past the sheet.
