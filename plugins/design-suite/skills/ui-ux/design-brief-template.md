# Design brief template

Copy the headings below. Fill each from supplied or observed material. Where nothing supports a line, write `MISSING INFORMATION: <what is needed and who could supply it>`. Never fill a gap with a plausible guess. Label every statement as observed, supplied, interpretation or recommendation.

```
# Design brief: <short name>
Status: draft for product owner review     Date: <date>     Author: AI design perspective (not user research)

## 1. User
Who is doing this? Role, experience level, frequency.
- Observed/supplied: ...
- MISSING INFORMATION: ...

## 2. Task
The job in one sentence from the user's side, plus the success outcome they would recognise.

## 3. Context
Device, location, interruptions, connectivity, time pressure, data sensitivity, what they did just before and after.

## 4. Evidence
| Item | Type (code / screenshot / analytics / feedback / interview) | Source and date | What it shows |
List only what was supplied or inspected. If there is no user evidence, say so here.

## 5. Constraints
Technical (stack, existing components), content, legal (including licence and attribution constraints), accessibility, deadlines, data ownership. Product owner decisions already made.

## 6. Current experience
Observations of what exists now, with file paths or screenshots. No judgement yet.

## 7. Proposal
The smallest coherent change. For each affected screen: layout, content hierarchy, controls, copy, and the state set (empty, loading, partial, error, success, offline, permission-denied) from flow-and-states.md. Responsive and accessibility behaviour stated explicitly.

## 8. Trade-offs
Options considered, why this one, what it costs, what it gives up. Name decisions that belong to the product owners (product, pricing, priority).

## 9. Open questions
Numbered, each with an owner and what would resolve it.
1. MISSING INFORMATION: ...

## 10. Acceptance criteria
Checkable statements. Each is observable by someone who did not write it.
- Given <state>, when <action>, then <visible result>.
- Keyboard: <path> works with no pointer.
- States: every state in section 7 is implemented and reachable in review.
- Test needed with real people: <task, who>. Not yet done.
```

## Checks before returning the brief

- Every claim about users has a source or is labelled interpretation.
- No numbers (conversion, task time, usage) appear unless supplied; recommended values are labelled "recommended".
- The proposal is the smallest change that meets the task; extras are listed as options, not bundled.
- Each acceptance criterion could fail. If it cannot fail, rewrite it.
- Open questions are specific enough that the product owner can answer in one line.
