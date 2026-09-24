# A/B testing: vocabulary and a trustworthy workflow

Randomized controlled experiments (A/B tests) answer one narrow question well: whether a specific change causes a measurable difference in a specific metric, for the population actually exposed to it. Use this reference to plan and read tests honestly rather than to manufacture statistical cover for a decision already made.

## Vocabulary worth being precise about
- **Randomization unit** — what gets assigned to a variant (user, account, session, device, or a cluster). Choose one that avoids the same person seeing both variants and matches how the analysis will run.
- **Control / treatment** — the baseline and the changed experience. Control isn't automatically the incumbent; it's whichever arm the others are measured against.
- **Primary metric vs. guardrails** — one prespecified metric answers the causal question; guardrails (latency, errors, revenue, unsubscribes) catch harm without being optimized against.
- **MDE (minimum detectable effect)** — the smallest effect the test is designed to reliably catch, given traffic, power, and duration — a planning input, not a claim about the smallest effect worth caring about.
- **Power** — the probability of detecting a real effect of a given size, under the study's assumptions.
- **P-value** — how surprising the data would be if the null hypothesis were exactly true. Not the probability the null is true, and not a measure of practical importance.
- **Confidence interval** — a range from a procedure that, run repeatedly, covers the true effect the stated proportion of the time — not a Bayesian probability statement unless a Bayesian method was actually used.
- **Credible interval** — the Bayesian analogue: a probability statement about the effect given the model, prior, and data.
- **Sample ratio mismatch (SRM)** — the observed split deviating from the intended allocation by more than chance. It signals broken plumbing; investigate before trusting any effect from that run.
- **A/A test** — identical experiences in both arms, used to sanity-check the pipeline. A "significant" result can still appear by chance — that's expected, not proof of a bug.
- **Multi-arm vs. factorial** — a multi-arm test compares several variants to one control; a factorial design varies multiple factors at once and estimates their combined and individual effects. Different designs, different analysis — don't conflate the terms.

## Before anyone is exposed
1. State the decision, the causal hypothesis, the segment, the primary metric, and the mechanism connecting change to metric. A before/after comparison or a split on an uncontrolled variable (like OS) is not concurrent random assignment.
2. Define eligibility, the assignment unit, allocation, exposure logging, the outcome window, exclusions, and any interference risk between arms (shared households, marketplaces, social features).
3. Pick an analysis method from the platform's current documentation or a qualified analyst — not a formula copied from an unrelated source. Record the baseline, the effect worth shipping, the sample/precision target, min/max run time, and the stopping rule. A Bayesian design needs its own documented prior and model; there's no universal "95% posterior" threshold.
4. Decide in advance how multiple variants, metrics, and any subgroup comparisons get handled statistically. A pattern found outside that plan is a lead for a follow-up test, not a result to act on.
5. Check instrumentation before trusting results: SRM, missing/duplicated events, exposure consistency. Platform-managed randomization doesn't exempt a test from data-quality checks, and a clean A/A run is informative, not a guarantee.
6. Launch only within existing authorization, with bounded exposure, guardrails, a rollback path, and an accountable owner. Watching guardrails for safety differs from repeatedly peeking at the primary metric and stopping the moment it looks good — use a deliberate sequential method, or commit to a fixed horizon.

## Reading and reporting results
Report sample size, exclusions, effect size in actionable units, uncertainty, method and prior, guardrail status, data-quality findings, and duration. "Not statistically significant" isn't proof of zero effect — distinguish harm, promising-but-inconclusive, and precisely-negligible results. Users self-selecting into one experience is not a randomized comparison, however it happened. Decide against the rules set in advance, then keep watching for effects that surface later.

## When it's the wrong tool
Low-traffic products, unusually risky changes, and *why* questions rather than *whether* questions are often better served by observation, interviews, or a pretotype (see [pretotyping](pretotyping.md)). There's no universal minimum-traffic threshold — it depends on the effect size worth detecting, so check it rather than assuming traffic is enough: a sample-size calculator such as [Evan Miller's A/B test sample size calculator](https://www.evanmiller.org/ab-testing/sample-size.html) takes a baseline rate and the smallest effect worth detecting and returns the subjects needed per variant. When that number exceeds realistic traffic within a tolerable duration, the honest conclusion is that an A/B test is the wrong tool for this decision right now — not a reason to lower the bar, run it anyway, or let it run indefinitely hoping to get there. Never withhold an obvious, low-risk fix just to wrap a test around it.

## Public references
- [Evan Miller's A/B test sample size calculator](https://www.evanmiller.org/ab-testing/sample-size.html) — used above to check whether available traffic can reach significance before committing to a test.
- Kohavi, Tang, and Xu, *Trustworthy Online Controlled Experiments* (Cambridge University Press, 2020) — the standard reference for experimentation pitfalls including SRM, novelty effects, and peeking.
- [Microsoft Research: diagnosing sample ratio mismatch](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/)
- [GrowthBook: Bayesian model updates](https://www.growthbook.io/blog/bayesian-model-updates-in-growthbook-3-0) — one illustration of why a specific platform's statistical engine should be read from its current documentation rather than assumed.

## Outputs
Use the [experiment worksheet](../templates/ab-test.md) to capture the plan and the readout, explain one concept at a time at the point the user needs it, and link the chosen metric back to the metric catalog. Diagram assignment and analysis flow with Lucid or Mermaid if it helps communicate the design; report actual statistical output for result charts, never an illustrative placeholder presented as real data. A redline pass can improve the plan's clarity; it cannot establish that the underlying statistics are valid.
