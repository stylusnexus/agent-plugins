---
name: recap-table
description: Use when the user asks to recap, summarize, or show work as a table; wants a before/after or what-changed comparison; asks "what did you change", "recap that", "show me a table"; or invokes /recap-table. Works in any project.
---

# Recap Table

Render a recap as a scannable comparison table so what changed is legible at a glance.

## The output IS this

A GitHub-flavored markdown table. Default columns:

| Area | Before | After |
|------|--------|-------|

- **One row per meaningful change** — an area, component, behavior, or decision that actually moved. Never a row per file or per commit unless that IS the unit that changed.
- **Left column** names the dimension in 1–4 words. **Middle** = the prior state. **Right** = the new state.
- **Cells are plain English**, terminal-legible, no jargon soup, no trailing punctuation. Aim for ≤12 words per cell; wrap longer ones naturally.
- **No filler rows.** If an area didn't change, it's not in the table. A 3-row table that captures the real deltas beats a 10-row one padded with noise.

## Pick the column set to the recap's shape

| Recap is about… | Columns |
|-----------------|---------|
| A change with a clear prior state (default) | `Area \| Before \| After` |
| Work delivered, no meaningful "before" | `Item \| Status \| Notes` |
| Impact framing | `Change \| What it does \| Why it matters` |
| Decisions taken | `Decision \| Chose \| Instead of` |

Default to `Area \| Before \| After`. Switch only when a "before" genuinely doesn't exist.

## Example

> Recap of the checkout refactor:

| Area | Before | After |
|------|--------|-------|
| Payment retries | Fixed backoff, synchronized clients | Exponential backoff with jitter |
| Guest checkout | Blocked behind login wall | One-tap, email captured post-purchase |
| Error surface | Generic "something went wrong" | Field-level messages with recovery CTA |

## When NOT to use

A single-fact answer or a one-line result. A table for one change is heavier than a sentence — just say it.
