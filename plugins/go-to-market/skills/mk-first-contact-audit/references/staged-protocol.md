# Staged cold read

A stranger decides whether a page is for them in seconds, in stages: the URL and headline first, the top of the page next, the whole page last. This protocol reproduces those stages so each one can be read, and scored, on its own.

## Step 0: write down the truth before reading anything

Ask the owner for three lines and keep them out of every reader's context:

1. **The one-line truth.** What the product is, for whom, and the problem it solves, in the owner's own words.
2. **The intended first visitor.** One person, not a market.
3. **The one action** a visitor should take next (join a waitlist, try it, read the docs).

If the owner cannot write line 1 in one sentence, stop. That is a positioning gap, not a page problem: hand it to `mk-positioning`.

## The four slices

| Slice | What the reader gets | How to cut it | Time it stands for |
|---|---|---|---|
| Stage 1 | URL, browser tab title, main headline | The rendered tab title and the first visible headline. If the headline rotates words, give the first state and say so | about 1 second |
| Stage 2 | Everything visible without scrolling, plus a screenshot | A 1440 by 800 window. Add a 390 by 844 phone view if mobile traffic matters | about 10 seconds |
| Stage 3 | The whole page, in reading order, plus a full-page screenshot | Visible text top to bottom; skip cookie banners | about 30 seconds |
| Machine view | The raw HTML a crawler without JavaScript receives | `scripts/static_signals.py` output, or the saved raw HTML | not timed |

If the host cannot render a page or take a screenshot, give the reader the text slice only and mark every visual finding `NOT VERIFIED`.

## Run each stage in a fresh context

Each stage goes to its own `cold-reader` run (or, without the agent, its own fresh conversation using [the brief](cold-reader-brief.md)). Stage 2 gets stage 2's slice, which includes what stage 1 showed, but never stage 1's answers. Answers carried forward anchor the next stage and hide where understanding actually arrived.

Do not tell a reader the product's category, its audience, that the page is under review, or that it is thought to be weak. Do not give it reviews, comments or the owner's description.

Never click "Sign in", join a waitlist, or create an account to get a slice. What sits behind a sign-in is `NOT VERIFIED`.

## Score in a separate step

The reader never scores itself. After all stages return, compare each answer to the truth from step 0:

- **Who:** matched, partly matched, or missing.
- **Problem:** matched, partly matched, or missing.
- **Differentiation:** does the reader say why this beats what it already uses, and is that the owner's real reason? Count `not stated` as missing.
- **Time to confidence:** the first stage at which confidence is 70 or more and who and problem both match.
- **Flags:** any stage with confidence below 70, every term the reader called unexplained, and every point where its answer conflicts with the truth.

Record each stage's answers verbatim next to the scores.

## What the reader can and cannot tell you

An AI reader finds the category of almost any product within one stage, because it has seen thousands of similar pages. A real stranger often cannot. So:

- Use the AI reader to **find** problems: unexplained terms, a headline and subhead that say different things, a call to action that does not match the situation, claims every product in the category makes.
- Do **not** score a page on whether the reader's category guess was right. A page can pass that and still leave a person unable to say why it helps.
- Score **differentiation recall** and **time to confidence** instead, and treat confidence below 70 as a flag.
- Use **people** to grade. Reader leniency means a page that passes the AI reader can still fail humans; a page that fails the AI reader almost certainly fails them.

A reader also cannot judge visual hierarchy, taste, or motion well from a screenshot. Say so in the scorecard rather than rating them.

## The human test

Five people from the product's intended audience, one at a time. Show the first screen for ten seconds, then hide it and ask:

1. In one sentence, what is this and who is it for?
2. What would it do for you that you do not already do another way?
3. Would you try it or join, and what would you do first?

Write down the answers word for word, and how long each person took to answer the first question. Do not explain the product, hint, or correct them.

**Default pass bar (a proposal the owner sets; it has no statistical basis, and five people is a small-sample convention, so treat a miss as a reason to fix the page and test again, not as a precise score):**

- At least 4 of 5 can say in one sentence what it does and who it is for.
- At least 3 of 5 name one thing it does that their current approach does not.
- At least 3 of 5 would try it or join. Stated intent is weak evidence; read it last.

Recruit from the audience, not a generic panel. A reader outside the audience produces false failures, and some visitors will say outright that they may not be the audience; note that when they do. Recruiting is outreach: draft the ask with `mk-outreach` and let the owner send it.

## Machine view

Give a second reader only the raw HTML. Ask whether it could confidently describe, cite or recommend the product. Then compare the static title, headings and text to the rendered page. A large gap means crawlers and link previews see something different from visitors.
