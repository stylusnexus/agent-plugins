# Structure and context

Rules for what the bot says, how it asks, and what it remembers. Each rule has a check you can run on a script of turns.

## 1. Four copy checks for every bot line

Review each reply against these. Mark failures with the line and the reason.

| Check | Fail example | Check by |
|---|---|---|
| True | Promises an action the bot cannot do ("I've cancelled it" when it only filed a request) | Compare each claim with what the back end really did |
| Only as long as needed | Three sentences before the answer | Delete the first sentence; if nothing is lost, it was padding |
| Relevant | Offers a tip unrelated to the user's last message | Ask: does this serve the goal stated in this flow? |
| Plain | Internal term, jargon, or an idiom a non-native reader may miss | Read as someone new to the product; flag any term not on screen elsewhere |

## 2. Mirror the input

When the bot acts on something the user typed, show it back in the confirmation: "Booking a table for 4 on Friday 7 pm." Check: for every slot collected, the next bot turn displays the value it understood, so a wrong reading is visible at once.

## 3. Optimistic UI needs a way back

If the interface shows success before the server confirms (message sent, order placed), specify the rollback: what the user sees if it fails, and how to retry or undo. Check: script a forced failure; the transcript must change from success to a clear failed state, never stay green.

## 4. Bounded choices over open questions

- Prefer two to three labelled options or suggestion chips (recommended range) to an open "What can I help with?".
- Avoid questions a bare "yes" can answer when you need a value: ask "Which day: Thursday, Friday or another day?" rather than "Do you want to book?"
- Check: list every bot question; mark each open, yes/no, or bounded. Flag open questions that appear where the valid answers are known.
- The option the user picks appears in the transcript as their message, so the history reads as a real conversation. Check: tap a chip and confirm the history shows what was chosen.

## 4a. Test whole paths, not single messages

A message can be fine alone and wrong in sequence. Run the full script from opener to goal and look for repeated questions across turns, contradicting replies, and the same chips shown after they were used. Check: no question is asked twice in one path unless the user changed their answer.

## 5. Entry point changes the opener

The opener should depend on where the user came from (a product page, an order page, an error screen, a marketing link, a voice wake word). Check: list the entry points; each has its own first line, or a recorded reason it shares one. Where the referrer is unknown, mark MISSING INFORMATION.

## 6. Say it is a bot

- Say early that this is an automated assistant and what it can do. Do not imply a person: no human name or photo for a bot, and no typing indicator that is staged to look like human typing.
- Check: the first screen contains a plain statement of what the assistant is and one sentence on what it can handle.

## 7. Context carry-over

| Rule | Check |
|---|---|
| For intent and slot bots: keep the last 1 to 3 turns of key details (recommended range). For language-model assistants, state what is kept and when it is cut or summarised (MISSING INFORMATION if unknown) | Ask "How much is it?" after naming an item; the bot answers about that item |
| Resolve pronouns to the last named thing | Say "change it to Friday"; "it" binds to the last order or booking, or the bot asks which |
| Set a timeout and announce it | After the idle limit, the bot says it no longer holds the earlier details instead of guessing |
| Say when context is gone | A new session opens with "I do not have your earlier request" and offers to restart |
| Repeat the user's own term | If the user says "reservation", the bot does not switch to "booking"; scan replies for synonym drift |

The timeout length is a product decision. Mark it MISSING INFORMATION if no figure is supplied.

## 8. Ask for personal data with a reason

When the bot asks for an email, phone, location or ID, say why in the same message, at the moment of asking, and say what happens if the user declines. Check: every data request in the script has a reason and a decline path. For consent and data-handling review, use `ui-ux` `ethics-and-consent-review.md`.
