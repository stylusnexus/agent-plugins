# Voice, measurement and chat surface

## 1. Personality

Personality comes from consistent word choice and rhythm. Humour is optional and risky: a joke that fails, repeats or lands on a frustrated user costs more than it gives.

- Write down personality principles: three to five short rules with a do and a do-not (recommended size). Example: "Short sentences. Name the user's item. No exclamation marks on errors."
- Check: take two replies for the same situation from two different writers; with the names removed, a reader should read them as one voice. Flag the pair if not.
- Check: error and refusal replies follow the same principles as happy-path replies. Humour is absent from errors unless the product owner chose it.
- Tone-of-brand is the product owner's decision. Offer options and the reasons.

## 2. Voice-only interfaces

- Use voice where hands or eyes are busy (driving, cooking, a workshop). Check: the flow names the hands-busy context; if there is none, ask whether voice is needed.
- Do not map a screen UI one to one onto speech. Lists of ten options, tables and long confirmations do not work by ear. Check: no turn lists more than three options aloud (recommended).
- Confirm destructive actions ("Delete all reminders. Say yes to confirm."). Check: a script of a destructive command always includes a confirmation turn, and a mishearing cannot delete.
- Do not read aloud what is already visible on screen. Check: a reply with a screen does not repeat the screen.

## 3. Measure where flows fail

Do not invent data. If none is supplied, mark MISSING INFORMATION and specify what to log.

- Count drop-off per flow: users who start versus users who reach the goal, and at which step. Recommended review trigger: more than 50 percent drop-off in a flow, then read the transcripts at the step where most leave. This is a trigger to look, not a quality verdict.
- Count steps from the platform entry point (home screen icon, widget, link, wake word) to the first core action. Check: write the count into the review and compare it with the equivalent screen flow.
- Log fallback hits, handoffs, retries per slot and repeated questions.
- Pair numbers with transcript reading and a test with real people (NEEDS-TEST).

## 4. Chat accessibility

Details live in accessibility-review `forms-and-errors.md` and `component-patterns.md`.

| Rule | Check |
|---|---|
| New messages are announced politely and do not take focus | Use `role="log"` on the transcript, or one polite `role="status"` region that is always in the page. While a reply streams, do not announce each chunk: announce that the assistant is replying, then the finished reply (see `forms-and-errors.md` in accessibility-review) |
| Focus after send stays in the input | Send a message; focus remains in the field, and the user can type again |
| Suggestion chips are reachable by keyboard | Tab reaches each chip; Enter or Space picks it; the chosen text appears in the transcript |
| Errors are named in text | A failed send says so in words, not only in colour |

Mark each NEEDS-TEST until run with a browser and a screen reader.

## 5. Mobile

See `mobile-design`.

- Keyboard overlap: the input and latest message stay visible when the keyboard opens. Check at a phone viewport with the keyboard up.
- Thumb reach: send and chips sit in the lower part of the screen, with targets sized per `mobile-design`.

## 6. States of the chat surface

See `ui-ux` `flow-and-states.md`. Specify each:

- Empty first run: a short statement and bounded starters.
- Typing or working indicator, honest about waiting.
- Failed send with a retry; offline with queued or blocked sending.
- Long streamed replies: readable while streaming, with a stop or cancel control that keeps what has arrived. The stop control is a keyboard-reachable button with a text name, pressing it does not move focus out of the input, and the partial reply stays, marked as stopped.
- Check: force each state in a script and confirm a visible, worded state exists.

## 7. AI-specific states

- The model may be wrong or unsure. Check: there is wording for uncertainty, and the interface does not present guesses as facts.
- Cite sources where the reply draws on them. Check: a factual claim from documents links to its source.
- The user can correct or undo: edit the last message, regenerate, or reverse an action taken. Check: each action the assistant takes has an undo or a confirmation.
- Do not pretend to be human; see `structure-and-context.md`.
