---
name: pm-discovery
description: "This skill should be used when the user asks to evaluate feature requests, identify assumptions, plan interviews, apply the Kano model, validate demand, design experiments, or run a product pre-mortem."
---

# Product Discovery and Experiments

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use only the sections needed for the current decision.

For early demand tests, read [pretotyping lessons](references/pretotyping.md). These draw on public Savoia materials, not a full-book extraction. For market structure and external context use `pm-market-analysis`; use `pm-visuals` for discovery loops and experiment diagrams.

## Workflow
1. Identify the user, job/context, decision, and desired outcome. Trace requests to problems; a loud request is evidence of that request, not proof of broad demand.
2. Synthesize available interviews, support reports, analytics, and observations. Keep references to source material and distinguish quotes, observations, interpretations, and hypotheses. Do not simulate users and present the simulation as research.
3. For interviews, ask about a specific recent episode, trigger, steps, consequences, alternatives, and workarounds. Use neutral wording; avoid leading with the proposed solution or relying only on “would you use this?” Interpret lack of a workaround cautiously: it may reflect constraints, not lack of importance.
4. Map assumptions across value, usability, viability, and feasibility. Include ethics and go-to-market risks under viability where relevant, including channels, pricing, and adoption. Invite risk challenges from any discipline rather than assigning exclusive ownership of a risk category. Include who is affected and evidence quality. Prioritize by consequences of being wrong, uncertainty, exposure, and cost of learning; do not reduce risk to development effort alone.
5. Compare plausible solutions and the no-build alternative. Design the smallest useful test of the riskiest assumption. Prefer observed behavior, task performance, or meaningful commitment where appropriate. Treat opinions as context, not equivalent to demand or payment. When a cheap first test passes, don't treat that as a build signal by itself — see [pretotyping](references/pretotyping.md) for the conditional concierge follow-up test, the repeat-use bar, and the maintenance/support-hours gate.
6. For each experiment specify: hypothesis, segment, method, observation/metric, baseline if available, proposed threshold and rationale, sample/recruitment constraints, duration or stopping condition, costs, risks, owner, and the decisions for pass/fail/inconclusive. Predefine criteria where possible; small convenience samples do not establish broad statistical proof.
7. Keep experiments within authorization. Do not send outreach, charge money, publish a fake door, collect unnecessary personal data, or run production experiments merely because a discovery plan proposes them. Prepare reviewable drafts before seeking any required authorization.
Assess experiment effects on revenue, reputation, customer experience, and sales/support operations. Define relevant notification, rollback, and monitoring needs before any authorized live test. Compare expected learning with cost; an inconclusive or poorly targeted experiment can be waste too. Prefer a simpler method when available traffic cannot support the proposed statistical test.
8. Run a proportional pre-mortem for substantial bets: possible failure, supporting evidence or uncertainty, consequence, prevention/detection, and owner. Classify launch blockers, follow-up items, and monitoring concerns. Speculation remains speculation.
9. Record what was learned, what remains uncertain, and the change to the decision. Feed back to strategy, value proposition, objectives, or roadmap rather than automatically creating more features.

## Output
- Decision and evidence summary.
- Problem themes and alternatives.
- Assumptions with risk rationale.
- Experiment cards with pass/fail/inconclusive decisions.
- Pre-mortem when relevant.
- Recommendation: build, test, defer, reject, or investigate, with rationale.
- What this plan can't tell you: name it explicitly (a small test's result says nothing about total market demand, long-term retention, or real acquisition cost — state that limit rather than letting the reader extrapolate past what was actually measured).

## Teach while working
Explain the difference between an assumption and a finding using the actual evidence. Offer one neutral interview question or a smaller experiment that could overturn the current recommendation.

## Adaptable prompt
“Evaluate this idea against our objective and evidence. Identify value, usability, viability, and feasibility assumptions, compare alternatives, and propose small behavioral tests. Specify what would change our decision and distinguish unsupported beliefs from findings.”

## Kano model
Use the [Kano workflow](references/kano.md) when assessing expected basics, performance attributes and delighters. It covers paired questions, response classification, mixed findings, conceptual diagrams and strategy-aware prioritization. Do not infer survey findings from team opinion.

## Sources and automation
Read [discovery sources and automation](references/insight-sources.md) to combine sources grouped by what people say, what people do, what the market shows, and what we generate ourselves; plan connector-assisted collection and generate a local evidence digest. Use the bundled `../../scripts/discovery_digest.py` for deterministic provenance checks; keep synthesis and source-quality judgment explicit.

## Discovery, risk and handoff connections
Read [discovery streams](references/discovery-streams.md) for initial versus continuous discovery, and [product risks](references/product-risks.md) for explicit risk responses and residual risk.

For research interviews, read [research-interviews](references/research-interviews.md).

For ai assisted pm, read [ai-assisted-pm](references/ai-assisted-pm.md).

For journey mapping, read [journey-mapping](references/journey-mapping.md).

For ab testing, read [ab-testing](references/ab-testing.md).
