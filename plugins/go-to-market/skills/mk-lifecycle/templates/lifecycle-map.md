# Lifecycle map

One row per stage the team can actually detect. See [lifecycle stages](../references/lifecycle-stages.md) for the underlying model: a stage's default behavior is to move forward only — automation should express "this contact reached stage X," never "this contact might have left it." Don't add a stage nobody has a way to observe; that's a wish, not a stage.

| Stage | What moves someone into it (the real, observable trigger) | Source of truth (where this is actually recorded) | What moves them to the next stage |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## Disengagement is a separate signal

The stage property above only moves forward. Track "stalled" or "gone quiet" separately — don't reuse a lifecycle stage to mean it.

| Disengagement signal | What it means | What (if anything) sends |
|---|---|---|
| | | |

## Gaps

- **Stages we'd like to track but can't detect yet:** [name them, and what instrumentation would need to exist first]
- **Contacts this map doesn't have a home for yet:** [note rather than force-fit]

---

## Example (fictional)

| Stage | What moves someone into it | Source of truth | Next stage trigger |
|---|---|---|---|
| Signed up | Account created | product database | Completes first real action |
| Activated | Completes first real action | product database | Returns and repeats the action in week 2 |
| Retained | Returns in week 2+ | product database | Starts a paid trial |
| Customer | First payment recorded | billing system | — |

Disengagement signal (fictional): no login in 21 days after Activated → send a single check-in, not a stage change.
