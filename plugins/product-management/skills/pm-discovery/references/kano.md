# Kano: customer satisfaction and feature decisions

Use Kano when the decision concerns how a specific segment responds to an attribute being present versus absent. It complements strategy, value-proposition design and prioritization; it does not replace them.

## Method
Explain these categories in plain language: must-be (expected basics), one-dimensional/performance (more fulfillment improves satisfaction), attractive (unexpected benefits), indifferent, and reverse (preference for absence). Questionable is a response-quality flag.

For each clearly defined attribute ask a functional question about its presence and a dysfunctional question about its absence. Both use five choices: like, expect/must be, neutral, tolerate/live with, dislike. Classify each paired response with this evaluation table; rows are functional and columns dysfunctional:

| Present / absent | Like | Expect | Neutral | Tolerate | Dislike |
|---|---|---|---|---|---|
| Like | Q | A | A | A | O |
| Expect | R | I | I | I | M |
| Neutral | R | I | I | I | M |
| Tolerate | R | I | I | I | M |
| Dislike | R | R | R | R | Q |

A=attractive, O=one-dimensional, M=must-be, I=indifferent, R=reverse, Q=questionable.

Method reference: [Rapid computation and visualization of data from Kano surveys in R](https://pmc.ncbi.nlm.nih.gov/articles/PMC6263047/). Table 1 documents this convention; identify the convention if combining datasets.

## Guided workflow and safeguards
1. Start with the product decision, segment, context and concrete attribute. Explain why Kano fits this question. If the user has no research, help draft a study; tentative team classifications are hypotheses, never survey findings.
2. Draft one question pair together. Example: “If you can export your project as a PDF, how do you feel?” / “If you cannot export your project as a PDF, how do you feel?” State any assumed alternative. Avoid bundling unrelated features or implying the preferred answer.
3. Pilot for comprehension. Record exact wording, recruitment, segment, date and limitations. Sending surveys or contacting participants requires applicable authorization; creating drafts does not.
4. Preserve raw paired responses and classify each. Report A/O/M/I/R/Q counts, missing answers, denominator and segment breakdown. Do not force a dominant label through a tie or hide a split audience. Investigate questionable responses and reverse preferences without silently recoding them.
5. Explain the decision implication alongside strategic fit, customer outcome, cost, dependencies and risk. A must-be label does not mean every proposed implementation is necessary; an attractive label does not mean “build next.” Kano does not measure willingness to pay, market size, actual adoption or feasibility.
6. Revisit when the segment, context or offering changes. Connect the result to the value proposition and roadmap, and validate behavior through other discovery methods when the decision needs it.

## Deliverables and diagrams
Deliver a study/question sheet or an evidence-backed classification table, a visual when useful, and a recommendation with limitations. Prefer Lucid through pm-visuals; Mermaid is the fallback for a category/decision map. For classic curves use an appropriate Lucid or local SVG chart: horizontal axis attribute fulfillment, vertical axis satisfaction. Label curves conceptual, not fitted survey results. Do not position individual features numerically without defensible data; a category map is often clearer. Keep reverse/indifferent responses and uncertainty visible in the accompanying table.

## Review checks
No invented respondents, votes or categories; pair wording preserved; table orientation correct; all counts reconcile; mixed results retained; hypotheses visibly distinct from research; prioritization rationale includes more than Kano.

## ProductCompass: needs-first interpretation
Additional source: Paweł Huryn, *Kano Model: How to Delight Your Customers Without Becoming a Feature Factory*, July 13, 2024. Source originals are not included; use the bundled guidance and Markdown worksheets.

Before classifying a requested feature, identify the underlying customer need, desired outcome and use context. Compare alternative ways to meet that need, including a smaller change or no build. This preserves Kano's usefulness without turning requests into an automatic delivery queue.

For the author's needs-first conceptual diagram, label the horizontal axis **extent to which the need is met**, and the vertical axis **customer emotional response**. Keep it distinct from the classic attribute-presence questionnaire. Do not silently replace survey questions with vague needs language and assume the resulting data is equivalent; define and pilot any adapted instrument. Diagrams remain conceptual unless supported by measured data.

Distinguish emotional response from an assessment of how well an outcome is currently achieved. If opportunity analysis is used alongside Kano, define its importance and fulfillment questions separately, document the scoring convention and retain uncertainty. Survey ratings are reported perceptions, not automatically objective measurements. The article's overlay of emotional responses on opportunity scores is explicitly a heuristic, not a validated conversion or mathematical ranking.

### Apply the source critically
- The article associates must-haves with high importance and delighters with lower importance. Do not infer importance from a Kano category; investigate both for the actual segment and context.
- “Fully fulfilled” is not an instruction to pursue unlimited perfection. Define an evidence-based acceptable outcome and review cost, risk and opportunity cost.
- Retain indifferent and reverse results; they can reveal unwanted complexity or segment differences even when the main teaching diagram shows only three curves.
- More functionality is not universally better. Define what improvement means: lower search latency, for example, moves in the opposite numeric direction from greater capacity.
- Expectations can change; recheck the segment over time instead of enforcing a universal category-transition schedule. The article's sentence about must-haves becoming performance is not adopted as an automatic rule.
- A value proposition also informs discovery hypotheses and testing. Do not confine it exclusively to go-to-market communication merely because the source contrasts those activities.

Teach with one real need: clarify the desired outcome, draft the question pair or explicitly labelled conceptual hypothesis, inspect the evidence, then explain what Kano adds and what still requires another method. No category alone authorizes building a feature.
