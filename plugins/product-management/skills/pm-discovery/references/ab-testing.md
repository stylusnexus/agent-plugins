# A/B testing: glossary and guided workflow

Source: Paweł Huryn, A/B Testing 101 + Examples, July 29, 2023. The article is useful introductory material but its statistical shortcuts are not adopted uncritically.

## Glossary
- Randomized experiment: assign eligible units to variants by chance under a defined allocation; compare outcomes for a causal question subject to design validity.
- Control/treatment: the reference and changed experiences. The reference can itself be a new design.
- Randomization unit: user, account, session or cluster receiving assignment; choose to avoid contamination/interference and match analysis.
- Primary metric: the prespecified main outcome; guardrails monitor important harms.
- MDE: minimum detectable effect used in planning; distinguish it from the smallest effect worth acting on.
- Power: probability of detecting a specified effect under the design/model assumptions.
- P-value: how incompatible the observed data are with the specified null model; not the probability the null is true.
- Confidence interval: interval from a procedure with stated repeated-sampling coverage; not automatically a posterior probability interval.
- Credible interval/posterior probability: Bayesian results conditional on the likelihood, prior and data.
- Sample ratio mismatch (SRM): evidence that observed assignment counts differ unexpectedly from intended allocation; investigate before effect interpretation.
- A/A test: identical variants used to exercise measurement/assignment; random false positives remain possible.
- Multi-arm test: several variants. Multivariate/factorial designs vary multiple factors; these terms are not interchangeable.

## Plan before exposing users
1. Identify the decision and causal hypothesis: segment, change, primary metric, plausible mechanism, practical effect and guardrails. A before/after comparison or assignment by operating system is not the same as concurrent randomized allocation.
2. Specify eligibility, stable assignment, unit, allocation, exposure logging, outcome window, exclusions and interference risks. Preserve assigned-group analysis; do not filter on post-treatment behavior casually.
3. Select an appropriate statistical method with the platform's current documentation or a qualified analyst. Record baseline, practical effect, traffic/variance assumptions, sample/power or precision plan, minimum duration/full cycles, maximum duration and stopping/decision rules. Bayesian methods also need planning and model/prior choices; a posterior “95%” threshold alone is not a universal rule.
4. Predefine multiplicity handling for variants/metrics and planned segment comparisons. Treat new subgroup patterns as exploratory; seek follow-up rather than cherry-picking a winner.
5. Check instrumentation, assignment/exposure consistency, missing outcomes, SRM and representative logging. Do not skip data-quality checks because a platform performs randomization. An A/A check is diagnostic, not guaranteed flat data.
6. Run only with appropriate authorization, bounded exposure, guardrails, rollback and accountable response. Monitoring safety/data quality is distinct from repeatedly stopping a fixed-horizon analysis when a favorable result appears. Use a justified sequential method when intended.
7. Report sample and exclusions, effect size in meaningful units, uncertainty, method/prior, practical relevance, guardrails, data-quality findings, duration and limitations. “No significant difference” does not prove equality; distinguish harm, promising, inconclusive and sufficiently precise negligible effects.
8. Decide ship/iterate/stop/continue under the declared rules; retain learning and monitor longer-term effects. User self-selection between interfaces changes interpretation; do not call an opt-in comparison randomized.

Use another method for scarce traffic, inappropriate exposure or questions better answered by observation/interviews. Do not delay an obvious critical fix for an experiment. No universal MAU cutoff applies. Templates and scripts are aids; this suite does not implement a statistical inference engine.

## Primary-source corrections
[Microsoft Research on SRM](https://www.microsoft.com/en-us/research/articles/diagnosing-sample-ratio-mismatch-in-a-b-testing/) supports assignment-quality checks before interpreting effects. [GrowthBook's model update](https://www.growthbook.io/blog/bayesian-model-updates-in-growthbook-3-0) describes prior-dependent posterior estimates, illustrating why the article's older engine descriptions should not be treated as permanent specifications. Consult live platform guidance before calculations. The article's numeric examples, expected-loss descriptions and Gaussian shorthand are not reusable calculation rules.

## Outputs
Use the [experiment worksheet](../templates/ab-test.md), explain one concept at the user's current step, and link outcome measures to the metric catalog. Use Lucid/Mermaid for assignment and analysis flow if helpful; use real statistical outputs for result charts. Redline can review the plan and narrative, not establish statistical validity.
