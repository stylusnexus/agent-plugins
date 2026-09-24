---
name: pm-objectives
description: "This skill should be used when the user asks for objectives, OKRs, key results, key metrics, success measures, a North Star metric, or product measurement."
---

# Objectives and Key Metrics

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use only the sections needed for the current decision.

## Workflow
1. Trace the requested objective to a strategic choice and user/business outcome. Clarify the period and constraints. If direction is missing, make that dependency explicit; avoid inventing strategy to fill a metrics table.
2. Select a small number of objectives for the period. Express a meaningful desired change, not a task list. Add two to four measurable key results only where useful, without treating this count as a quota.
3. Distinguish **outcome** (user or business change), **output** (delivered artifact), **input/leading indicator** (influencing behavior), **lagging indicator** (result), and **guardrail** (harm or deterioration to avoid). Track delivery milestones separately from evidence of product success.
4. For every metric define the name, purpose, numerator/denominator or exact calculation, population/segment, time window, source/query, baseline and date, target and rationale, owner, review cadence, and decision it informs. For non-ratio measures state the unit and aggregation. Avoid ambiguous counts such as “active users.”
5. Mark missing baselines unknown and propose how to measure them. Label proposed targets as provisional until agreed; do not dress arbitrary percentages up as benchmarks. Distinguish an observed change from an attributable product effect.
6. Consider a North Star metric only if it represents repeatable customer value. Explain its causal hypothesis and useful input metrics. Do not force a single metric onto a product with multiple distinct jobs. Pair growth/usage measures with quality, retention, cost, trust, or reliability guardrails as relevant.
7. Inspect gaming and misleading averages: bots, repeated events, cohort mix, vanity metrics, sample size, seasonal effects, and segment differences. Never infer retention from aggregate growth or causation from correlation.
8. Define review actions: continue, investigate, change the bet, or stop. Connect these measures into the roadmap work and turn open questions into discovery experiments — internally that means the `pm-roadmap` and `pm-discovery` skills, but describe it to the user as the next step in plain words, not by those file names. Route instrumentation implementation to existing analytics specialists only when authorized.

Use `pm-teams` for empowered-team ownership, collaboration, and operating-model guidance.

## Embed team objectives in strategic context
Frame each team objective as a consequential customer or business problem plus clear measures of success. Include mission/vision/winning aspiration reference, target segment and job, relevant where-to-play/how-to-win choices, why this problem now, evidence, constraints/trade-offs, guardrails, dependencies, decision rights, and review cadence. State what the team may change independently and which strategic choices require the owner.

Explain why: context lets a team discover better solutions, resolve trade-offs, and avoid improving one metric at the expense of user value or another team. Assign problems and outcomes rather than preselected feature lists disguised as objectives. Align across teams through shared strategic intent and dependencies; do not mechanically cascade arbitrary percentages or assume every team controls a company-level result. For a solo builder or AI-assisted workflow, translate “team” into the responsible person/agent and preserve the same context. AI work completed is not evidence of customer outcomes.

Use the [team objective brief](templates/team-objective-brief.md) for substantial handoffs.

## Output
- Objective and linked strategy, period, and owner.
- Key results with baseline, target, evidence status, and deadline/review date.
- Metric definitions and source availability.
- Guardrails and leading indicators.
- Unknowns, instrumentation gaps, and decision/review rules.

## Teach while working
Use the user's own draft to show why “ship onboarding” is an output and successful first use is a candidate outcome. Do not invent the meaning or target of successful first use; define it from actual user value.

## Adaptable prompt
“Translate this strategy into a small set of objectives and measurable key results. Define key metrics precisely, distinguish delivery from outcomes, preserve unknown baselines, justify provisional targets, and add guardrails and review decisions. Explain the most important measurement choice in plain language.”

## Working through an OKR cycle
Read [OKR cadence](references/okr-cadence.md) for setup, check-ins, guardrails, end-cycle learning and contextual adaptations.

## Practical reference
Use [North Star selection and glossary](references/north-star.md) and the [40-entry metric catalog](references/metrics-catalog.md) to choose and define measures. Retrieve candidates with the bundled metrics lookup; do not track all metrics by default.
