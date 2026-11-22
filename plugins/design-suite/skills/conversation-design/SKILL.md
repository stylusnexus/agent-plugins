---
name: conversation-design
description: "Use when designing or reviewing a chat, assistant, bot, voice or messaging interface: conversational copy, bot replies, suggestion chips, intents and fallbacks, repair of failed or misunderstood input, context across turns, handoff to a human, bot personality and tone, or the interface around an AI chat (typing, streaming, stop, retry, uncertainty). Also for measuring where conversations fail."
---

# Conversation design

Make a conversation finish the user's task without making them repeat themselves, guess what to type, or get stuck. This is an AI design perspective on the script, the flow and the chat surface. It is not user research, conversation analytics or evidence about what any user says.

## When to use

- Writing or reviewing bot copy, openers, reprompts and error replies.
- Specifying a flow that collects input (dates, names, emails, choices) over several turns.
- Deciding what happens when the bot misunderstands, is unsure, or cannot help.
- Specifying the chat screen itself: states, accessibility, mobile keyboard, AI-specific states.
- Reviewing a voice or messaging experience, or a handoff to a person.

## Workflow

1. Identify the user, their goal and the entry point (page, app, message channel, voice). Mark unknown intents, traffic and drop-off MISSING INFORMATION.
2. Write the happy path as a script of turns, then list every input that can fail (`repair-and-recovery.md`).
3. Review each bot line against the four copy checks and the choice rules (`structure-and-context.md`).
4. Specify context carry-over, timeouts, and the point where a human takes over.
5. Specify the chat surface: states, accessibility, mobile, and AI-specific states (`voice-and-measurement.md`). For forms-style input, use the accessibility-review `forms-and-errors.md`.
6. Write personality principles and the measures that will show where flows fail (`voice-and-measurement.md`).
7. Return the per-flow output below with evidence tags (VERIFIED from the supplied script or code, NEEDS-TEST with real people), MISSING INFORMATION, and the checks not performed.

## Reference files

| File | Open when |
|---|---|
| `structure-and-context.md` | Reviewing bot copy, choosing between open and bounded questions, openers by entry point, transcript behaviour, context across turns, asking for personal data |
| `repair-and-recovery.md` | Designing failure paths: bad input, low confidence, fallback, slots, retries, reprompt wording, escape and handoff |
| `voice-and-measurement.md` | Personality and voice rules, voice-only interfaces, drop-off measures, and chat-surface checks (accessibility, mobile, states, AI states) |

## Output format

Per conversation flow:

1. User and goal (with MISSING INFORMATION).
2. Happy path as a numbered script of turns.
3. Repair paths per input: failure case, reprompt, exit.
4. Escape and handoff rules.
5. Context rules: what carries, for how many turns, timeout, how loss is announced.
6. States of the chat surface.
7. Voice notes.

Then trade-offs, open questions, a **Checks not performed** list (for example: no screen reader run, no real transcripts, no voice device), and acceptance criteria that a named script of turns can check (for example: "Script R3: user enters a past date twice; the bot offers three dates and a human option; no third identical prompt").

## Boundaries

- This is not user research or conversation analytics. Do not invent intents, traffic, confidence scores or drop-off data; mark them MISSING INFORMATION.
- Numbers labelled "recommended" are defaults for the product owner to confirm, not measurements.
- Product owners keep product decisions and tone-of-brand decisions. Offer options and reasons.
- Do not publish, deploy or contact users.
- This skill reviews and specifies conversation design. It does not train, tune or configure any model or intent engine.
- Respect privacy and consent boundaries; point to `ui-ux` `ethics-and-consent-review.md` for data requests.
