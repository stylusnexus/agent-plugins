# Data states, provenance and alerts

The central rule: missing data must never look healthy. Absence of a signal is not a clear signal.

## 1. Provenance and freshness on every external signal

Show, or make reachable in one step:
- Source: which system provides it (and which team or service owns it).
- Retrieved at: when the dashboard last got it, as absolute time plus relative ("2026-10-21 09:14, 3 h ago"). Show the time zone, or use local time and say so.
- As of: when the underlying fact was true, if different from retrieval time.
- Method: live, polled, cached, or manually entered, if it affects trust.

Keep this quiet when fresh (small, secondary text) and loud when not. Do not make users hover to find out a number is old; on touch there is no hover.

## 2. State table

Define each state per signal. Every signal needs a visible representation for each row.

| State | Meaning | Display | Never |
|---|---|---|---|
| Loading | request in flight, no value yet | stable placeholder of final shape | show zero or a previous value as current |
| Normal / confirmed clear | source reported recently and shows no issue | value plus freshness | |
| Empty (valid) | source reported and there is genuinely nothing | explicit "None" with freshness | blank space |
| Stale | last report older than the tolerance | last value, dimmed or flagged, with age and the tolerance | present as current or as healthy |
| Partial coverage | some sources or items missing | value labelled "from N of M sources", name what is missing | sum available parts as if total |
| Unavailable | source errored or is unreachable | "Unavailable", reason if known, retry, last known value with age | show 0, a dash with no explanation, or green |
| Not configured | no source connected | say so and how to connect, if the user can | treat as healthy |
| Unknown / MISSING | status cannot be determined | "Unknown" in the attention layer | collapse into OK |

Tolerance for staleness is per signal and depends on how fast it changes and how costly delay is. Recommended: set tolerance as a multiple of the expected refresh interval (for example, stale after missing two expected updates) and have the product owner confirm. Do not invent a number without the interval. If the interval is unknown, mark MISSING INFORMATION.

## 3. Aggregates and roll-ups

- A parent status that rolls up children takes the worst known state, and unknown or unavailable children must not be ignored. "All clear" requires every child to be confirmed clear and fresh.
- Show how many children contributed.
- Totals over partial data carry a visible "partial" label at the number, not only in a footnote.

## 4. Loading and refresh

- First load: placeholders in the final layout so nothing jumps.
- Refresh: update in place; keep old values visible with a subtle indicator rather than blanking the page.
- Show that a refresh failed without discarding the last good values.
- If auto-refresh changes content under the user, avoid moving the element they are reading; announce changes only where they matter (status message, not focus theft).
- Provide a manual refresh and show its result.
- Skeleton placeholders match the final tile dimensions so layout shift stays near zero when data lands. Give assistive technology a text status ("Loading"), since a skeleton says nothing.
- Perpetual motion on tiles is off by default. Animate only where a value changes or an action is confirmed. Looping tile animation also raises WCAG 2.2.2 problems for content that moves automatically.
- Animate a reorder (shared-element move) only when the order actually changes.

## 5. Errors on a dashboard

Per-widget errors stay local. One failing source must not blank the page. The error says which source, what is affected, last good time, and the next step (retry, link to the provider or owner). The page-level attention layer should list failing sources as items.

## 6. Thresholds

- Thresholds belong to a decision. For each: what action follows when it is crossed, who acts, and what normal looks like.
- Do not invent thresholds. Use supplied targets or SLOs; otherwise MISSING INFORMATION, and show the value without a status colour until a threshold is agreed.
- Prefer few levels (for example OK, needs attention, failing). More levels need distinct actions.
- Avoid single-sample flapping: consider requiring a condition to persist or using hysteresis. Value to be chosen with the owner; no default is given here.
- Show the threshold in the chart or beside the number so users can see distance to it.
- Never use colour alone; add text, icon or shape. Check contrast of status colours on their background.

## 7. Alert design

- Alert only on conditions where someone should act. Everything else is a dashboard item, not an interruption.
- Each alert states: what, where, since when, impact if known, and the first action or link.
- Group related alerts; deduplicate repeats; show count and first/last time.
- Severity maps to channel: only the highest warrants interrupting. Channel choice is a product owner decision.
- Acknowledgement and snooze, if offered, record who and when; they must not hide the underlying condition. Writing acknowledgements back to the source needs a reviewed design for writes.
- An alert that cannot fire because its source is down is itself an attention item.
- Resolve states visibly; do not just delete the alert.

## 8. Acceptance checks

- Disconnect or delay each source in turn: the dashboard shows Stale or Unavailable, never Normal.
- Return an empty valid result: shows an explicit none with freshness.
- Remove one of N sources: totals are labelled partial.
- Every number can be traced to a source and time.
