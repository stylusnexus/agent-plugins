---
name: pm-value-proposition
description: "This skill should be used when the user asks for a value proposition, customer value, alternatives, a value curve, a strategy canvas, or eliminate-reduce-raise-create choices."
---

# Value Proposition and Value Curves

Honor applicable repository instructions and prefer a project-local version of this skill when present.

Read [shared principles](../product-manager/references/principles.md) before applying this workflow independently. Use only the sections needed for the current decision.

Read [value design and messaging](references/value-design.md) for deeper development and messaging. Use the [working sheet](templates/value-proposition.md) to draft with the user.

## Workflow: value proposition
1. Select one segment and job/use context. Avoid blending unrelated audiences into a universal promise.
2. Map the current situation, desired outcome, pain and consequences, workarounds, and alternatives. Include doing nothing or manual work where relevant.
3. Explain the mechanism by which the product changes that situation, the resulting benefit, and why it matters relative to alternatives. Separate capabilities from benefits and proof from promises.
4. Draft a plain-language value proposition: “For [people in context] who need [job/outcome], [product] helps [benefit] through [mechanism]. Compared with [alternative], it offers [meaningful difference], supported by [evidence or validation needed].” Treat this as a thinking aid, not mandatory marketing syntax.
5. Link each major claim to evidence, an assumption, or a proposed test. Mark unsupported willingness-to-pay and superiority claims as hypotheses. Do not fabricate testimonials or research.

Keep positioning (the chosen competitive context), value proposition (the promised customer value), messaging (what to communicate), and copywriting (the expression) distinct. Strong copy does not validate the proposition.

## Workflow: value curve
Read the framework sources in `../product-manager/references/sources.md` when explanation or attribution is needed.
1. Establish the segment and decision the curve will inform. Identify factors buyers actually consider from research; label provisional factors when research is absent.
2. Compare current alternatives, the current product where it exists, and a separately labelled proposed offering. Use the same factors, order, scale, and time basis for all series.
3. Define what each factor and scale means. A curve represents relative offering level, not an objective overall quality score. Keep customer importance separate. Higher price, more customization, or more functionality is not automatically better. Explain direction for cost, time, complexity, or effort factors.
4. Record each rating's source, date, rationale, and confidence. Use unknown for missing information; never silently convert missing values to zero. Do not join across unknown ratings in a chart as though they were measured. Label illustrative numbers and future targets prominently.
5. Produce a comparison table first. Where supported by the data, generate a labelled line chart with a legend and accessible table, using available visualization tools. With inadequate evidence, return an honest provisional qualitative table and research plan rather than a fabricated quantified curve.
6. Explore **eliminate, reduce, raise, create** choices. For each state the customer benefit, cost/capability consequence, sacrifice, and assumption. Look for a coherent different shape rather than a higher score on every factor. Check that claimed cost reduction and differentiation are supported by the activity choices.
7. Recommend how to validate whether customers value the difference and whether the builder can deliver it economically. Route experiments to `pm-discovery`, strategic decisions to `pm-strategy`.

## Output
- Segment, job, before/after, alternatives, and value proposition.
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
