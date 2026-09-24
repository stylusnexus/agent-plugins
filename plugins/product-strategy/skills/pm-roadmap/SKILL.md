---
name: pm-roadmap
description: "This skill should be used when the user asks for a roadmap, prioritization, now-next-later plan, product sequencing, or a feature backlog linked to outcomes."
---

# Outcome-Based Roadmaps

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use only the sections needed for the current decision.

## Workflow
1. Read the accepted direction, objectives, current capabilities, existing backlog and commitments, research, constraints, and dependencies. Reconcile live issue state when available; do not treat old issue titles as proof work remains.
2. Map requests to the underlying problem and objective. Merge overlapping problems conceptually while preserving source IDs. Compare alternatives, including a smaller intervention, build vs. buy/partner, or no build. Stop condition: if diagnosis turns up several plausible causes with no single failure point isolated, say so and propose narrowing the diagnosis (or a small test to isolate it) as the next step — don't roadmap a fix for a cause that hasn't actually been pinned down. For whichever goal on this roadmap currently has the least evidence behind it, start interviews or another cheap evidence pass on that goal now, in parallel with the rest of the planning, rather than waiting for it to come up in priority order.
3. Prioritize using user impact, strategic fit, evidence/confidence, risk, effort/capacity, dependencies, and opportunity cost. Include operational obligations and blockers. Use qualitative judgments with uncertainty when numbers are unavailable; do not invent RICE inputs or rank solely by coding speed.
4. Classify work as discovery, delivery, or measurement. For high-consequence uncertainty, schedule the smallest useful test before expensive delivery. Do not demand research theater for a verified, low-risk fix.
5. Build a Now / Next / Later roadmap by default. For each entry include the user problem, outcome/objective, bet or initiative, evidence, major dependency, owner if known, success measure, and next decision. Keep Later tentative.
6. Show capacity limits, sequencing rationale, rejected/deferred alternatives, and explicit non-goals. Label dates as commitments, estimates, or horizons. Do not derive business timelines from token generation speed; include integration, human decisions, research, operations, and validation.
7. Define review cadence and promotion/stop rules. Update the roadmap when learning changes the rationale, without silently changing the user's mission or strategy.
8. For an initiative ready for delivery, prepare only the needed brief: problem, target user, objective, evidence, scope/non-goals, smallest first slice, key flow, assumptions, dependencies, acceptance criteria, rejected/deferred options, outcome measures, a dates table marking each date estimate vs. commitment, rollout and monitoring. Scale the brief to the decision; avoid mandatory full-size documents for small changes.
For delivery handoff, distinguish product instrumentation (usage/outcome evidence) from health monitoring (errors, latency, availability). Include release dependencies, gradual exposure or feature flags when appropriate, rollback/disable path, accountable responder, and user/support communication. Prefer small independently releasable changes where feasible; do not assume flags or deployment infrastructure exist. A/B testing requires appropriate traffic and design, not just a working toggle. Route technical implementation to the existing engineering workflow.
9. Handoff to the project's existing issue/planning workflow. Drafting a roadmap does not itself authorize coding, publishing issues, or promising dates to others.

## Output
- Roadmap with outcome links, scope, horizons, capacity assumptions, risks, and dependencies.
- Why this order; what is deferred and what would change the order.
- Discovery and measurement work alongside delivery.
- Brief for the next initiative only if requested or necessary.

## Teach while working
Explain one prioritization trade-off and the difference between a roadmap as a set of bets and a backlog as an inventory of possible work.

## Adaptable prompt
“Turn these initiatives into an outcome-based roadmap. Reconcile existing work, compare alternatives, show evidence and dependencies, and recommend what belongs in Now, Next, and Later. Explain trade-offs, preserve uncertainty, and separate delivery completion from learning whether the outcome improved.”

## Kano model
Use the [Kano workflow](../pm-discovery/references/kano.md) when assessing expected basics, performance attributes and delighters. It covers paired questions, response classification, mixed findings, conceptual diagrams and strategy-aware prioritization. Do not infer survey findings from team opinion.

## Discovery, risk and handoff connections
For a PRD, read [PRD lifecycle](references/prd-lifecycle.md) and use the [initiative brief](templates/initiative-prd.md). Link [risk decisions](../pm-discovery/references/product-risks.md) rather than treating delivery readiness as certainty.

## Stories and slices
Read [user stories and delivery slices](references/user-stories.md) when drafting stories, job stories, acceptance criteria or splitting initiatives.

## Outcome roadmap coaching
Read [outcome roadmaps](references/outcome-roadmaps.md) when choosing roadmap detail, distinguishing goals from features, or reviewing delivery commitments. Use the [working roadmap template](templates/outcome-roadmap.md) to draft Now / Next / Later with evidence and explicit decision conditions.
