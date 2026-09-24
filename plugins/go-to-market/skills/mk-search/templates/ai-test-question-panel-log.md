# AI test-question panel log

Log template for the method in [the AI test-question panel](../references/test-question-panel.md). One row per (question, assistant, run date). Re-run after any page change this skill's workflow touches, plus one scheduled check in between.

## Panel questions

*A dozen or so real buyer questions — a direct "what is X," a comparison against the two or three products people actually compare this to, and a couple of specific-use-case questions pulled from real support or sales conversations. Not a keyword-research list.*

| # | Question | Where it came from (real conversation, not invented) |
|---|---|---|
| 1 | | |
| 2 | | |

## Run log

| Date | Assistant | Question # | Mentioned at all? | Cited as a source, or just described? | Position in answer (first / mid / buried / absent) | Other products named alongside |
|---|---|---|---|---|---|---|
| | | | | | | |
| | | | | | | |

## Reading the log

- One "not cited" result on one run is a reason to re-check, not a reason to declare failure — assistants' answers vary between runs on an identical question.
- Only call a pattern real once it holds across more than one run.
- Where a source is independently checkable (Google states AI Overview/AI Mode traffic already appears in normal Search Console reporting — see the [reference file](../references/test-question-panel.md)), cross-check the panel's read against that log rather than trusting the panel alone.

## Follow-ups triggered by this run

*What, if anything, changes on the page as a result — link the specific section that needs a rewrite, not a general "improve SEO" note.*

→

---

### Example (fictional)

*Illustrative only — a made-up product and made-up run, no real-world numbers.*

| Date | Assistant | Question # | Mentioned? | Cited or described? | Position | Other products named |
|---|---|---|---|---|---|---|
| 2026-09-01 | (assistant name) | 1 | Yes | Described from general knowledge, no link | Mid-answer | Two competitors, both linked |

Follow-up: question 1's answer suggests the product page never states its core feature as a plain, quotable sentence near the top — rewrite the opening section per [citable writing](../references/citable-writing.md).
