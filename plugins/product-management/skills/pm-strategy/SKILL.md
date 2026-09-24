---
name: pm-strategy
description: "This skill should be used when the user asks for product strategy, where to play, how to win, trade-offs, cost leadership, cost focus, differentiation, or differentiation focus."
---

# Product Strategy and Trade-offs

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use only the sections needed for the current decision.

## Purpose
Build a coherent set of choices, not a collection of goals. Read `../product-manager/references/principles.md` before strategic recommendations. Use the Playing to Win choice cascade when useful, without forcing every project through every framework.

For workshops, ongoing strategy review, and collaboration, read [working with strategy](../product-manager/references/working-with-strategy.md).

## Workflow
1. Diagnose the situation from current evidence: target users, unmet need, alternatives including doing nothing, product capabilities, constraints, and what has changed. Separate evidence, inference, and assumptions.
2. Establish the winning aspiration. If unsettled, use `pm-vision`. Do not silently redefine an accepted mission or aspiration.
3. Develop two or three coherent options. For each connect: **winning aspiration → where to play → how to win → required capabilities → management systems**. Iterate between choices; this is not a waterfall. Management systems include ownership, decision cadence, measures, and resource allocation, even for a solo builder.
4. Specify where to play: segment, job, use context, geography when relevant, channels, and scope. Specify how to win: why those users choose and keep this product over real alternatives, and what activities make that possible.
5. Compare advantage and scope explicitly:

| Strategic option | Scope | Basis of advantage | Test the claim |
|---|---|---|---|
| Cost leadership | Broad market | Structurally lower cost at acceptable value/quality | Identify sustainable cost drivers and comparable cost evidence |
| Cost focus | Narrow segment | Lower cost of serving that segment | Explain why specialization changes the economics |
| Differentiation | Broad market | Distinctive value customers care about | Test preference, use, retention, or willingness to pay |
| Differentiation focus / focused differentiation | Narrow segment | Distinctive value for particular needs | Test depth of fit and the limitations imposed by specialization |

Do not equate low price with low cost, high feature count with differentiation, or a small current user base with a deliberate focus strategy. Multiple advantages can coexist when activities support them; do not declare combinations impossible or claim to win on everything.
6. Inspect economics where relevant: relative costs, acquisition, onboarding, support, infrastructure/model usage, maintenance, distribution, pricing, and willingness to pay. Mark missing numbers unknown. For noncommercial tools assess time, reliability, effort, and sustainability without inventing a business model.
7. Write explicit trade-offs: chosen option, rejected alternative, benefit gained, value sacrificed, people not served, cost/capability consequence, and reconsideration trigger. Distinguish deliberate exclusions from temporary constraints. Do not erase safety, accessibility, or baseline quality requirements to make a curve look different.
8. Use `pm-value-proposition` to test the customer promise and value curve. Use `pm-growth` for acquisition/retention and distribution choices. Check capabilities and activities reinforce the promise; name current gaps and any plausible imitation barriers without inventing a moat.
9. Identify what must be true. Propose disconfirming evidence and the smallest useful tests via `pm-discovery`. Recommend a direction with uncertainty and the decision needed from the user.

For a full Product Strategy Canvas, use `pm-canvas`. Use `pm-capabilities` for business capability mapping and `pm-strategy-fit` for the explicit coherence/defensibility review.

Use `pm-market-analysis` when Five Forces, PESTEL, or SWOT would change the strategic decision. Use `pm-visuals` to produce diagrams alongside the analysis.

## Output: strategy brief
- Situation, mission/vision/aspiration reference, scope, and evidence.
- Options compared and recommendation.
- Five connected strategic choices, including capability gaps and review cadence.
- Value proposition, advantage/scope, growth logic, and economic assumptions.
- Trade-offs and explicit non-goals.
- Riskiest assumptions, evidence needed, and change triggers.
- Handoff to objectives and roadmap only at the necessary level of detail.

## Teach while working
Explain why one actual choice is strategic: which alternatives it rules out and how that affects the product. Show the difference between “grow revenue” as a goal and a choice about whom to serve and why they will choose the product.

## Adaptable prompt
“Compare coherent strategies for this product. Connect winning aspiration, where to play, how to win, capabilities, and management systems. Evaluate advantage and scope, identify trade-offs and what must be true, and recommend a direction supported by the available evidence. Separate a low selling price from a sustainable cost advantage.”

## Worked examples and critical comparison
Use [teaching examples](references/teaching-examples.md) when an example would help. The worked examples are real, sourced cases, each cited back to what the company or writer published about itself. Teach connections and critique metrics, trade-offs and defensibility before adapting a pattern to the user’s project.
