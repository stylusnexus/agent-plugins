---
name: pm-value-proposition
description: "This skill should be used when the user asks for a value proposition, customer value, alternatives, a value curve, a strategy canvas, or eliminate-reduce-raise-create choices."
---

# Value Proposition and Value Curves

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use only the sections needed for the current decision.

Read [value design](references/value-design.md) for how to develop the underlying value proposition from the working sheet's job steps and underserved outcomes; it also explains why positioning and messaging are separate, later work rather than covered here. Use the [working sheet](templates/value-proposition.md) to draft with the user.

## Workflow: value proposition
1. Select one segment and job executor — who is actually doing the job, which may differ from the buyer. Avoid blending unrelated audiences into a universal promise.
2. Name the job to be done: the functional task, plus its social and emotional dimensions. Then break it into the job steps the job executor moves through, independent of any solution.
3. For each step, capture the desired outcome statement the job executor uses to judge whether it's going well, with importance and current satisfaction where known. The underserved outcomes — important but poorly satisfied today — are where opportunity concentrates.
4. Name the alternatives the job executor uses today for these steps, including doing nothing and manual workarounds, and where each falls short on the underserved outcomes.
5. For each underserved outcome this offering addresses, state the mechanism — how the offering actually produces that change, kept separate from the outcome itself — with the evidence behind it. Separate the capability from the benefit, and the proof from the promise.
6. Draft the plain-language value proposition using the statement in section 6 of the [working sheet](templates/value-proposition.md), built from the job step, underserved outcome, mechanism, and alternative already captured. Treat it as a thinking aid, not marketing copy.
7. Link each major claim to evidence, an assumption, or a proposed test. Mark unsupported willingness-to-pay and superiority claims as hypotheses. Do not fabricate testimonials or research.

Positioning is separate, later work: April Dunford writes that "positioning defines what market you intend to win and why you deserve to win it" ([source](https://www.aprildunford.com/post/an-introduction-to-positioning)). Settle the value proposition first; polished copy does not validate it.

## Workflow: value curve
Read the framework sources in `../product-manager/references/sources.md` when explanation or attribution is needed.
1. Establish the segment and decision the curve will inform. Identify factors buyers actually consider from research; label provisional factors when research is absent.
2. Compare current alternatives, the current product where it exists, and a separately labelled proposed offering. Use the same factors, order, scale, and time basis for all series.
3. Define what each factor and scale means. A curve represents relative offering level, not an objective overall quality score. Keep customer importance separate. Higher price, more customization, or more functionality is not automatically better. Explain direction for cost, time, complexity, or effort factors.
4. Record each rating's source, date, rationale, and confidence. Use unknown for missing information; never silently convert missing values to zero. Do not join across unknown ratings in a chart as though they were measured. Label illustrative numbers and future targets prominently.
5. Produce a comparison table first. Where supported by the data, generate a labelled line chart with a legend and accessible table, using available visualization tools. With inadequate evidence, return an honest provisional qualitative table and research plan rather than a fabricated quantified curve.
6. Explore **eliminate, reduce, raise, create** choices. For each state the customer benefit, cost/capability consequence, sacrifice, and assumption. Look for a coherent different shape rather than a higher score on every factor. Check that claimed cost reduction and differentiation are supported by the activity choices.
7. Recommend how to validate whether customers value the difference and whether the builder can deliver it economically. Move testable claims into discovery work and strategic trade-offs into strategy work (internally `pm-discovery`, `pm-strategy`) — say that to the user as the next decision to make, not by the skill's file name.

## Output
- Segment, job executor, job to be done, job steps, and desired outcomes (with importance and current satisfaction where known).
- Underserved outcomes, today's alternatives, and the mechanism for each underserved outcome addressed.
- Draft value proposition statement (working sheet §6) with its evidence status.
- Claim/evidence/assumption table.
- Value-curve data with factor definitions, sources, confidence, and current/proposed distinction.
- Chart when defensible; otherwise the explicit data gap.
- Eliminate/reduce/raise/create choices and their trade-offs.
- Next validation step.

## Teach while working
Explain that the value proposition is the customer promise, while the curve compares the pattern of an offering against alternatives. A distinctive curve is a strategic hypothesis, not evidence of demand.

## Adaptable prompt
“Develop a value proposition for this segment and job, grounded in the attached evidence. Compare the meaningful alternatives using a value curve. Separate current facts from proposed differentiation, define rating scales, preserve unknowns, and explain what to eliminate, reduce, raise, or create and what those choices cost.”

## Kano model
Use the [Kano workflow](../pm-discovery/references/kano.md) when assessing expected basics, performance attributes and delighters. It covers paired questions, response classification, mixed findings, conceptual diagrams and strategy-aware prioritization. Do not infer survey findings from team opinion.
