# Repair and recovery

A conversation is the happy path plus every way it can go wrong. Specify both. A flow with only a happy path is not finished.

## 1. Repair path per input

For each input the bot collects, list how it can fail and write the reply for each. Every failure branch needs a reprompt and a way out.

| Input type | Failure cases to list |
|---|---|
| Date | in the past, too far ahead, a holiday or closed day, ambiguous order (03/04), words such as "next Friday", missing year |
| Time | 12 hour versus 24 hour, no am/pm, outside opening hours, time zone unstated |
| Email | missing @, typo in the domain, extra spaces, a name instead of an address |
| Name or item | unknown to the system, near match, two matches, different spelling |
| Number | zero, negative, decimal, words ("two"), over a limit |
| Yes/no | "maybe", "not sure", a question back, silence |

Check: build this table for the flow. Any row with no written reply is a finding.

## 2. Confidence cutoff and disambiguation

If the system gives a match confidence, the design needs a cutoff, and a designed reply below it.

- Above the cutoff: act, and mirror what was understood.
- Below the cutoff: ask a bounded question ("Did you mean A or B?") rather than a generic error.
- Cutoff value: recommended to be chosen with real logs by the product owner. Without data, mark MISSING INFORMATION and do not invent a number.
- Check: send an ambiguous script line; the reply names the likely options, not "Sorry, I did not understand".

## 3. Fallback intent and review cadence

Keep one explicit fallback for anything unmatched. Check: unmatched queries are logged, and a named person reviews the log on a stated cadence (recommended: weekly while the bot is new, then monthly). Without a cadence the bot never improves. This skill specifies the log and the review; it does not train the model.

## 4. Slots and value lists

- A slot that accepts only a fixed list silently misses values the list lacks (a new city, a new product). Specify the behaviour for an unlisted value: accept it as free text and verify, or offer the closest listed options.
- Check: enter a plausible value that is not in the list; the bot neither rejects it blindly nor accepts it unchecked.
- The same word can mean different things in different intents (a city versus a band, "order" as a purchase versus a sort order). Check: list words that appear in two or more intents and write how context chooses between them, or ask.
- Mark each slot required or optional. Prompt only for required ones; ask for optional ones once, or not at all.

## 5. Fast-fail versus multi-turn repair

| Style | Use when | Rule |
|---|---|---|
| Fast-fail: one retry, then switch path | Short task, cheap to restart, or another route is available | After the retry, offer chips or hand off |
| Multi-turn repair: guide step by step | Long or costly task, high stakes, much progress would be lost | Narrow the question each turn |

For both: set a maximum retry count and an exit. Check: script the same bad input repeatedly. The loop must end at the stated count. Recommended: two retries per slot; the product owner confirms.

## 6. Vary the reprompt

Repeating the same sentence feels like a broken machine. Write at least three variants (recommended) and make each add something: a hint, an example, then a different route.

Example progression for a date slot: "What date?" then "A day like 12 March works." then "I can show this week's open days instead."

Check: run the failure three times; no two consecutive replies are identical, and the third changes the route.

## 7. Escape and handoff

- Every step offers a way out: "Something else", "Start over", or a person.
- After the maximum retries, never end the chat or leave a dead end; offer the exit or a person. Check: after the last retry the bot presents the exit and does not close.
- Hybrid handoff: set a threshold for passing to a human, such as low confidence on repeated turns, a sensitive topic, a complaint, or a complex task. Check: the handoff passes the transcript so the user does not repeat themselves, and says how long a person typically takes (mark MISSING INFORMATION if unknown).
- If no human exists, say so, and give the written route that does exist (form, email, phone).
