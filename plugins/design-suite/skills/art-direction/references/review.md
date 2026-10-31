# Review — a fresh pair of eyes on the page

You judge your own page badly: you remember what you meant. The `direction-reviewer` agent sees only the
screenshots and the written sheet, never the code or your reasoning, and says where the page drifted from
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
reviewer as a fresh agent). The reviewer runs alongside your own look in step 8, not instead of it.

- **Hero checkpoint:** after step 6.2, when the first screen is built and nothing else exists. Drift
  caught here is not copied into ten sections.
- **Finish checkpoint:** after step 8 and before step 9. The motion layer is not built yet, so the
  reviewer lists it as unable to verify (`scenes.mjs` owns it).

Each mode runs once, plus at most one re-review after your fixes. The re-review is the next folder
(`<n+1>`) and is scoped to the earlier Blocks findings. A hero verdict of `fix first` means fix, then
re-review once; a second `fix first` on the hero goes to the user.

## 2. The packet

A folder, `.taste-skill/review/<n>/`, written by the lead. Nothing in it is written from memory: if a line
is not in `direction.json`, in a screenshot or report the scripts wrote, or in the user's own request, it
does not go in.

| File | Where it comes from |
| --- | --- |
| `packet.md` | The sheet as text, copied from the `direction.json` that `draw.mjs` wrote into its `--out` folder: direction id and one-line rationale; section order with each section's composition; type roles and sizes; palette as proportions; component rules for buttons, nav and footer; the `--have` assets. Then the number of redraws and which slots, and whether `--keep palette,type` was used. The first line is `kind: page`. |
| `claim.md` | The user's request verbatim, then the sheet's rationale line. The reviewer reads it last, after it has written its five-second read of the screenshots. |
| screenshots | Copied from `.taste-skill/inspect/`, which `inspect.mjs` writes: `desktop-fold.jpg`, `tablet-fold.jpg`, `mobile-fold.jpg` and the full-page sheets `desktop-page-NN.jpg`, `tablet-page-NN.jpg`, `mobile-page-NN.jpg`. Add scene frames only when the sheet deals scroll scenes. |
| old-page screenshots | Redesigns only: the before shots at 1440 and 390, copied from the before folder named in the redesign steps. |
| `report.json` | Redesigns only: the `.taste-skill/kept/report.json` that `keep.mjs` wrote. Its `dropped` list is the declared drops, so the reviewer does not flag them. |
| the hero review | Finish mode only: the hero checkpoint's verdict and findings, so a fix cannot quietly regress. |

**Hero mode** takes its shots by running `inspect.mjs` on the half-built page and copying only the three
`-fold.jpg` files. The page is not finished, so its WARN and FAIL lines mean nothing yet.

## 3. What is withheld

The reviewer must not see: source and CSS, your critique and its scores, your reasons for any redraw, the
per-section claims you wrote in step 2, and the inspector's WARN and FAIL list. Anything in that list is
withheld, so the review is not anchored on the meter or on your intent. Do not add notes, hints or
"known issues" to the packet.

## 4. Dispatching it

Start a fresh agent with an empty context (the `direction-reviewer` agent) and tell it only two things:
the review folder path and the mode, hero or finish. Do not paste the sheet, the screenshots or your
thoughts into the prompt; it reads the folder.

It returns one ranked "Do next" list of at most 7 items (plus a `go` or `fix first` verdict in hero mode),
per-slot verdicts of match, partial or miss, what it is unable to verify, and on redesigns what the old
page did better. Each finding has a severity: Blocks (it contradicts a stated sheet slot), Weakens (it
breaches a named law), or a taste note, which can never block.

## 5. Replying to the findings

Write `.taste-skill/review/<n>/replies.md`: one line per finding, in the finding's id order, each either

- `fixed` naming the screenshot that now shows it, or
- `disputed` quoting a sheet line that contradicts the finding.

A finding that contradicts a sheet slot (Blocks) cannot be disputed; fix it. Disputes are for law breaches
and taste notes only. An unanswered finding blocks the report: step 10 lists every finding with its reply,
and the lead reads `replies.md` before reporting. This extends the rule in step 7: do not argue with the
meter, and do not argue past the sheet.
