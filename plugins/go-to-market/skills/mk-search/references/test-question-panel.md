# AI test-question panel

The only reliable way to know whether an AI assistant cites you is to ask it the same questions a real buyer would, on a schedule, and write down what actually comes back — not to infer it from traffic numbers or guess from how well-optimized a page looks. This file is the method; the [log template](../templates/ai-test-question-panel-log.md) is where results live over time.

## Sizing the panel to what the team can act on
Don't build the panel by keyword-research habit, harvesting every possible query variant; size it by how many questions a small team can actually re-ask and read the answers to on a recurring basis. A reasonable starting point is a short list — a dozen or so — covering the handful of ways a real buyer actually phrases the decision: a direct "what is X" question, a comparison against the two or three products people actually compare you to, and a couple of specific-use-case questions pulled from real support or sales conversations, not invented ones. A panel of two hundred keyword variants nobody has time to review twice a quarter produces a spreadsheet, not information. Grow the list only once the smaller one is being reviewed reliably and is still leaving real questions unanswered — size follows capacity, not ambition.

## What to write down for each question
For every question, on every assistant tested: was the product mentioned at all; was it cited as an actual source, versus just described from the model's general knowledge; roughly where in the answer it showed up (first thing mentioned, buried at the end, or absent); and which other products got named alongside it. Those four things are what a small team can actually act on. A full taxonomy of named tracking metrics isn't necessary to make a decision from this data, and inventing one adds bookkeeping without adding a decision.

## Picking assistants to test
Test the assistants real buyers are likely to ask, not every assistant that exists. Where a source can be checked against real referral data, do it: Google states that AI Overview and AI Mode traffic already appears in standard Search Console reporting, so a claim like "cited in AI Overviews" from the panel is at least partly checkable against a real log, not just a one-off screenshot. (Source: Google, "AI features and your website," https://developers.google.com/search/docs/appearance/ai-features, accessed 2026-09-24.) For assistants without that kind of independent log, the panel itself — repeated, dated, and screenshotted — is the record.

## Cadence
Run the panel on a cadence tied to how often the team actually changes the content the panel is testing, not an arbitrary calendar interval. Re-testing weekly when nothing has shipped just produces the same answer with more rows; re-testing so rarely that a shipped fix goes unverified for months defeats the point. A reasonable default: re-run the panel right after any page change the `mk-search` workflow touches, plus one scheduled check in between so drift gets caught even when nothing shipped.

## What a result does and doesn't prove
A citation in one run of one assistant is a data point, not a trend — assistants' answers can vary between runs on the identical question. Only call a pattern real once it holds across more than one run; a single "not cited" result is a reason to re-check, not a reason to declare a page has failed.
