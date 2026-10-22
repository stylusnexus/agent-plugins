# Flow and states

Use this to review a task flow and to specify every state a screen can be in. All timing numbers are recommended starting values, not standards, unless stated. Confirm them against the product's own measurements; if none exist, mark MISSING INFORMATION.

## 1. Task flow review

1. State the task as one sentence from the user's side ("Rename a project", not "Use the settings form").
2. Name the start point (where the user is, what they know) and the end point (what proves success to them).
3. List every step, decision and wait between them. Count taps/clicks and fields.
4. For each step ask:
   - Is the next action obvious without reading instructions?
   - Does the user have the information needed here, or must they remember it from an earlier screen?
   - What can go wrong, and where does the user land afterwards?
   - Can they go back or cancel without losing work?
5. Mark steps that exist for the system's convenience rather than the user's (extra confirmation, redundant fields, forced account creation) as candidates to remove.
6. Check the unhappy and interrupted paths, not only the happy one: validation failure, lost connection, session expiry, browser back, reload, double submit, returning tomorrow.

Record findings as observation / interpretation / recommendation. Do not state completion rates or drop-off numbers unless supplied.

## 2. The full state set

Every data-bearing view and every action needs a decision for each state. A missing row below is a finding.

| State | What the user needs | Design rule |
|---|---|---|
| Empty (first use) | Why it is empty, and the one next action | Explain the value, offer the primary action, no blank panel |
| Empty (no results) | That the query worked and found nothing | Echo the filter or query, offer to clear or change it |
| Loading | That something is happening | Keep layout stable; skeleton of the final shape beats a spinner for content, spinner for short actions |
| Partial | What loaded and what did not | Show what is available, mark the missing part in place, offer retry for that part only |
| Error | What failed, whether data is safe, what to do | Plain language, inline near the cause, a recovery action |
| Success | That it worked and what changed | Confirm at the point of action, show the result, say what happens next if anything |
| Offline | That the device has no connection and what still works | Persistent, non-blocking indicator; queue or disable actions honestly |
| Permission-denied | That access is the reason, and who can grant it | Say what is blocked and the route to access; never show a generic error or a blank |

Also consider: stale (data older than expected), disabled (say why, near the control), read-only, and in-progress-by-someone-else.

## 3. Error recovery

- Say what happened, why if known, and the next step. No codes alone, no blame ("You entered an invalid value" becomes "Enter a date such as 2026-03-14").
- Put field errors next to the field and summarise them at the top of a long form, with links to each field.
- Preserve everything the user typed. Never clear a form on error.
- Offer a way forward that is not the same failing action repeated: edit, retry later, contact route, save draft.
- Distinguish user-fixable errors from system faults; for system faults say whether the work was saved.
- Retries: tell the user whether an automatic retry is happening; do not retry non-idempotent actions silently.
- Errors must not rely on colour alone; pair with icon and text.

## 4. Destructive and irreversible actions

Order of preference:
1. Make it undoable (undo toast, trash with restore period). Prefer this over asking.
2. If it cannot be undone, confirm with a dialog that names the object and the consequence ("Delete project Northwind and its 14 files?"), and label buttons with the verb ("Delete project", "Keep project"), not "OK/Cancel".
3. For high-consequence actions (data loss for many items, anything affecting other people), require typing the object's name or an equivalent deliberate step.
4. Default focus goes to the safe option. Destructive buttons are visually distinct but not the only large, coloured button.
5. Do not use confirmation for routine, reversible actions; people learn to click through.

Product owners approve any destructive behaviour that affects customer data or production.

## 5. Progressive disclosure

- Show what most people need most of the time; reveal the rest on demand (expand, "Advanced", detail view).
- Disclosure controls must be visible, labelled and keyboard-operable. Do not hide required fields or the only route to a task.
- Keep one level of disclosure where possible; nested reveals are hard to find and to return from.
- Defaults should be safe and sensible so that skipping the advanced options is fine.
- Summarise hidden state ("3 filters applied") so collapsed sections do not hide active settings.

## 6. Feedback timing (recommended values)

These follow widely used response-time guidance; treat as starting points to verify.

| Elapsed time | Recommended feedback |
|---|---|
| Up to about 0.1 s | Feels instant; no indicator needed |
| About 0.1 to 1 s | Acknowledge the action (pressed state, inline change); no spinner needed |
| About 1 to 10 s | Show a progress indicator; keep the interface responsive |
| Over about 10 s | Show determinate progress or steps and let the user leave or cancel; notify on completion |

Further rules: do not flash a spinner for operations that finish within a few hundred milliseconds (delay showing it, recommended about 300 ms, then keep it visible at least about 500 ms to avoid flicker). Success messages that auto-dismiss should stay long enough to read and must remain reachable by assistive technology (status message, not a focus theft). Anything that carries an error or requires action must not auto-dismiss (WCAG 2.2 timing guidance).
