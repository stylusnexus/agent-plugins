---
name: dashboard-design
description: "Use when designing, reviewing or fixing a dashboard, internal console, operations or status view, metrics page, KPI summary, chart or data table, or any data-heavy screen. Covers decision-first layout, freshness and provenance, missing/stale/partial data states, alert thresholds, number and chart choices, and review findings."
---

# Dashboard design

Make a dashboard answer the user's next decision or question quickly. A dashboard is not useful merely because it displays connected data. All guidance here is an AI design perspective; it is not user research or evidence about what any user needs.

## When to use

- Designing a new dashboard, console or summary view.
- Reviewing one that "isn't useful yet", is noisy, or looks healthy when it should not.
- Choosing charts, number formats, filters, thresholds or alert behaviour.
- Specifying loading, empty, stale, partial or unavailable states for external signals.

## Workflow

1. Identify the user, decision cadence and the decisions to support. Mark unknowns MISSING INFORMATION (`decision-first-layout.md`).
2. Inspect the existing dashboard and trace each displayed fact to its authoritative source and owner.
3. Prioritise by consequence and urgency. Separate attention items, summary and drill-down detail.
4. For every external signal show state, retrieval time and source where practical. Distinguish missing, stale, unavailable and confirmed-clear (`data-states.md`).
5. Design loading, error, empty, partial-coverage and normal states. Never imply all clear when sources are missing.
6. Choose number formats, charts, filters and time ranges per question (`metrics-and-charts.md`). Drop decorative charts and aggregate scores with no decision value.
7. Provide responsive layout and accessibility requirements; involve the mobile and accessibility roles where relevant. For a new look or a substantial redesign of the screen, use the art-direction skill in its app-screen mode.
8. Review the result with `review-checklist.md` and return an annotated proposal, rationale, open questions and acceptance criteria.

## Reference files

| File | Open when |
|---|---|
| `decision-first-layout.md` | Starting a design or restructuring one; deciding what goes on top |
| `data-states.md` | Any signal that can be late, missing, partial or wrong; thresholds and alerts |
| `metrics-and-charts.md` | Formatting numbers, choosing or critiquing a chart, filters, time ranges, drill-down |
| `review-checklist.md` | Reviewing an existing dashboard or checking your own proposal; findings format |

## Output format

Annotated proposal: user and decisions (with MISSING INFORMATION), source map (fact, owner, freshness), layout by priority, state table, chart and number choices with reasons, open questions, acceptance criteria. For reviews, use the finding format in `review-checklist.md`.

## Provenance and writes

- Every number shows where it comes from and how fresh it is. Preserve provenance and freshness.
- Read-only data stays read-only. Do not propose writing back from a display surface without a reviewed design for writes.

## Boundaries

- No invented metrics, targets, baselines or thresholds. Recommended values are labelled "recommended" and need product owner confirmation.
- Product owners keep product, pricing and priority decisions, including which numbers matter.
- Do not publish, merge, deploy or contact users. No new dependency or design system unless requested and reviewed (a chart library counts as a dependency).
- Respect the project's licensing and attribution constraints for any content shown.
