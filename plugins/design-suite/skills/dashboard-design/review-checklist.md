# Dashboard review checklist

This is an expert review by an AI design perspective. It does not replace testing with the product owners or other real users. Say which findings need that.

## Checklist

Decisions and layout
- [ ] Each user, decision and cadence is written down (or MISSING INFORMATION).
- [ ] Every element maps to a decision; unmapped elements are listed.
- [ ] Attention items, summary and detail are separate layers.
- [ ] Top-level numbers are within the recommended 3 to 6, or the excess is justified.
- [ ] The first screen supports the decision without hunting.

Truthfulness of state
- [ ] Each external signal shows source and retrieval time.
- [ ] Stale, partial, unavailable, not-configured and unknown are visibly different from OK.
- [ ] Roll-ups cannot read "all clear" while a child is unknown, stale or unavailable.
- [ ] Failing one source does not blank others.
- [ ] Loading never displays zero or old values as current.

Numbers and charts
- [ ] Units, period and scope are labelled; deltas name their baseline.
- [ ] Bar charts start at zero; truncated line axes are labelled.
- [ ] Chart type matches the question; no gauges, 3D, or dual axes without reason.
- [ ] Colour is not the only carrier of meaning; contrast meets 3:1 for graphics and 4.5:1 for text.
- [ ] Tables where exact values or actions matter.
- [ ] Dense views are unboxed; number columns use tabular figures; skeletons match final tile size.
- [ ] No looping motion on tiles by default.

Thresholds and alerts
- [ ] Each threshold has an owner and an action, and a source (supplied or MISSING INFORMATION).
- [ ] Alerts carry what, where, since when, first action.
- [ ] An alert whose source is down is surfaced.

Interaction and access
- [ ] Filters and time range visible, resettable, applied consistently.
- [ ] Drill-down preserves context and ends at source.
- [ ] Keyboard, screen-reader text alternatives, no hover-only information.
- [ ] Narrow-screen behaviour specified (mobile-design).

Authority
- [ ] Read-only data stays read-only; no write-back without a reviewed design for writes.
- [ ] Each fact shows its source and freshness.

## Finding format

```
ID: D-<n>
Location: <screen / widget / file path>
Type: observation | interpretation | recommendation
Severity: critical | major | minor | cosmetic   (critical = can mislead a decision, e.g. missing data shown as healthy)
What: <what is seen, factual>
Why it matters: <consequence for the decision>
Evidence: <screenshot, code reference, supplied source> or MISSING INFORMATION
Fix: <smallest change that resolves it>
Check: <how someone else verifies the fix>
Needs real-user test: yes | no
```

Order findings by severity, then by how many decisions they affect. Put misleading-state findings first. End with: what was reviewed, what was not, open questions, and the checks that need data access the reviewer did not have.
