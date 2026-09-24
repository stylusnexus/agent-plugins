---
name: pm-capabilities
description: "This skill should be used when the user asks for business capability modeling, a capability map, L1/L2 capabilities, current versus target capabilities, capability maturity, strategic capability gaps, or build/buy/partner choices."
---

# Business Capability Modeling

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use the smallest map that supports the decision; a solo project does not need enterprise ceremony.

## Define the right thing
Treat a business capability as a stable ability the business or project needs to achieve an outcome: **what it can do**, independent of its current implementation. Use clear noun-based names such as Customer Onboarding or Content Curation. Describe the ability in one sentence with explicit boundaries.

Distinguish a capability from a process (how work flows), a team (who performs it), a software application (what supports it), and a feature (a particular solution). Map those as supporting relationships; do not reproduce the org chart or application inventory as the capability map. For example, Customer Onboarding is an ability; verifying an account is a process step; Customer Success is a team; a CRM is software. Capability ownership does not imply one team performs all the work.

Support commercial products, internal tools, community projects, and personal software. Define the business or project boundary first. Do not mistake the customer's desired outcome for an ability the provider must possess; show their relationship.

## Workflow
1. Establish the decision, scope, mission/aspiration, accepted strategic choices, target users, desired outcomes, and constraints. Inspect existing maps and project evidence before inventing a taxonomy. Label candidate capabilities as proposed until their relevance and boundaries are checked.
2. Build a compact L1/L2 hierarchy. Use L1 for broad abilities and L2 for meaningful subdivisions. Give each a stable ID, name, definition, included/excluded scope, and parent where applicable. Keep levels at comparable granularity. Prefer two levels; add L3 only when a concrete decision requires it. Avoid duplicate abilities; represent cross-cutting relationships explicitly rather than copying a capability under multiple parents.
3. Validate coverage against the strategic choices and end-to-end customer outcomes. Identify missing abilities, overlapping definitions, and unclear ownership. Check both differentiating and essential supporting capabilities; generic industry maps are starting hypotheses, not evidence of need.
4. Assess current and target states separately. Attach evidence, source/date, scope, confidence rationale, and unknowns to each current assessment. Code existence or a vendor contract does not prove the ability works reliably. Specify the target as an observable ability and performance need, with a proposed horizon or accepted deadline. Never silently turn a target into current capability.
5. Use a simple, explicitly agreed rubric when maturity assessment helps. Assess relevant dimensions such as people, process, information, technology, and partners separately when they differ materially. Use the suggested rubric below as a local working tool, not a certified standard. Do not average ordinal ratings into spurious precision or treat every capability as needing maximum maturity.
6. Assess strategic importance separately from maturity. Explain whether an ability differentiates the product, enables a chosen strategy, or supplies an essential baseline, and why. Include reliability, safety, or required controls where relevant. Tie importance to evidence and accepted choices, not enthusiasm or speculative competitive claims.
7. Map dependencies across people/skills, processes, information/data, technology, and partners. Include management systems: accountability, decision rights, feedback measures, review cadence, and resource allocation. Mark dependencies unknown when not inspected. Surface shared bottlenecks, external reliance, and sequencing constraints.
8. Compare ways to close the consequential gaps: improve existing practice, build, buy, partner, combine approaches, defer, or stop pursuing the capability. Compare differentiation, total cost assumptions, time, available skills, integration, reliability, data/control needs, lock-in, reversibility, and ongoing operation. Verify current vendor facts before relying on them. Recommend options; do not purchase, contact vendors, or make commitments without authorization.
9. Connect each recommended gap closure to a strategic choice and measurable outcome. Carry that into the measurement and sequencing work next (internally `pm-objectives` and `pm-roadmap`) with capability ID, current evidence, required target, candidate intervention, dependencies, owner if known, acceptance evidence, and review trigger — describe this to the user as "turning this gap into a tracked bet," not by the skill names. Use the discovery workflow (`pm-discovery`) for uncertain assumptions. Preserve the distinction between capability outcomes and delivery initiatives.

## Suggested local maturity rubric

| State | Meaning | Evidence to seek |
|---|---|---|
| Unknown | Insufficient evidence to assess | Identify the missing observation or owner |
| Absent | Evidence shows the ability is unavailable within scope | Failed or unavailable outcome, verified boundary |
| Ad hoc | The outcome is possible through inconsistent or individual effort | Concrete examples and observed limitations |
| Repeatable | The ability works through a defined, repeatable approach | Repeated outcomes, responsibilities, supporting practices |
| Managed | Performance and exceptions are monitored and acted on | Measures over time, ownership, response evidence |
| Adaptable | The ability improves deliberately as needs change | Demonstrated learning and sustained adjustment |

Do not interpret absent documentation as an absent capability. Mark a partially supported assessment provisional and explain which dimension is uncertain. Choose sufficient target maturity for the strategy and constraints, rather than maximizing all scores. Define performance targets separately; maturity alone does not establish effectiveness or customer value.

## Deliver useful artifacts
For a substantial assessment, provide:
- Scope, decision, strategic references, evidence limits, and terminology.
- L1/L2 map with stable IDs, definitions, boundaries, and supporting relationships.
- Assessment table: capability ID, strategic role, current evidence/state, required target, gap, dependencies, and uncertainty.
- Prioritized recommendations with rationale, options, estimated effort/cost only where supported, sequencing, acceptance evidence, and revisit triggers.
- A concise handoff to the roadmap and unresolved decisions for the user.

Use a table or simple diagram when it clarifies the map. For a narrow question, answer directly with only the relevant capability slice. Keep project artifacts in the existing project documentation when writing is authorized; do not create global project memories.

## Teach while working
Explain one distinction using the actual project: “Payment Collection is an ability; integrating a payment provider is one way to support it.” Show why the distinction matters: the capability can stay stable while teams, processes, or software change. Explain how an observed gap affects a chosen strategy before suggesting tools. Label illustrative examples clearly and avoid quizzes unless requested.

When acting as a background specialist, return the map, evidence, recommendations, teaching notes, and focused questions to the parent. Keep interactive teaching and unresolved strategic decisions in the main conversation.

## Adaptable prompt
“Map the business abilities this strategy requires at L1/L2. Define their boundaries, distinguish them from processes, teams, features, and applications, and assess current versus target ability using evidence. Preserve unknowns. Identify strategic gaps and dependencies, compare build/buy/partner or simpler alternatives, and connect recommended changes to measurable outcomes and the roadmap.”

## Source orientation
The capability definition and restrained hierarchy align with [SAP LeanIX business capability modeling guidance](https://help.sap.com/docs/leanix/ea/business-capability-modeling-guidelines?locale=en-US). The workflow and rubric above are a practical synthesis, not a claim of compliance with or certification in an enterprise architecture standard. Read current primary guidance when a user requests a specific formal method.
