# Trustworthy experiments

"We ran a test and it went up" is not evidence on its own — how the test was built determines whether that number means anything. This reference covers what makes an experiment trustworthy, the ways experiments quietly go wrong, and what to do when you can't randomize at all.

## Set the sample size before you look at any data

Fix the sample size — or the running time — before the experiment starts, using a calculator such as [Evan Miller's Sample Size Calculator](https://www.evanmiller.org/ab-testing/sample-size.html), which takes a baseline rate, the smallest effect worth detecting, statistical power, and significance level, and returns how many subjects each variant needs. Checking results early and stopping the moment they look significant breaks that plan. Miller's ["How Not To Run an A/B Test"](https://www.evanmiller.org/how-not-to-run-an-ab-test.html) shows why: significance math assumes the sample size "was fixed in advance," and a test peeked at repeatedly and stopped on a good-looking moment can turn a nominal 5% false-positive rate into roughly 26%. Decide the number, then hold to it.

## What breaks trust after the test is running

The [ExP Platform](https://exp-platform.com/) site — built from Ron Kohavi's experimentation team at Microsoft, running large-scale online controlled experiments since 2006 — names recurring ways a "significant" result still isn't trustworthy:
- **Sample ratio mismatch** — the actual traffic split doesn't match what was configured, "a symptom for a variety of data quality issues" that invalidates the comparison before you read the metric.
- **Short-term movement that doesn't hold** — a metric can move immediately and reverse over time, so a short window can report the opposite of the real effect.
- **Metric-reading mistakes** — Dmitriev, Gupta, Kim, and Vaz's KDD paper ["A Dirty Dozen: Twelve Common Metric Interpretation Pitfalls in Online Controlled Experiments"](https://exp-platform.com/Documents/2017-08%20KDDMetricInterpretationPitfalls.pdf) catalogs twelve recurring ways teams misread a metric that moved, even when the statistics behind it were run correctly — among them: treating an underpowered metric's non-movement as proof of no effect, declaring victory on a borderline p-value, peeking early and stopping the moment a result looks good, assuming a movement is uniform across segments when it isn't, letting outliers distort the read, mistaking a novelty or primacy effect (people react differently just because something is new) for a lasting one, and — Twyman's Law — treating an improbably large win as real instead of as a reason to check the plumbing first.

One primary metric decided in advance, one hypothesis, one decision rule — the more metrics get scanned after the fact for something significant, the more of what turns up is noise.

## Quasi-experiments when you can't randomize

Most marketing decisions — a pricing change with one price, a redesign shipped to everyone, a single-market launch — never got a proper control group. Treating the before/after difference as the effect ignores everything else that changed over that period. Two methods build a comparison anyway:

- **Difference-in-differences** compares the change in your metric against the change in a similar, untreated group over the same window, rather than just your own before/after. It depends on the "parallel trends" assumption — that your group and the comparison group were moving the same way *before* the change — so check that assumption on historical data before trusting the result.
- **Synthetic control** builds a comparison out of several untreated units instead of one, as a weighted combination chosen to track your unit closely before the change. [Statsig's overview](https://www.statsig.com/perspectives/synthetic-control-methods-test-groups) describes it as a "weighted combination approach [that] can estimate causal effects even when randomized trials aren't possible," and notes teams often pair it with difference-in-differences so the two methods can corroborate each other. It's also "incredibly sensitive to your choice of control units" — a badly matched comparison group is worse than no method at all.

Channel-level attribution is its own version of this problem. Rand Fishkin's SparkToro writeup argues a lot of what actually moves a channel — old-school word of mouth, a conference mention, someone telling a colleague — shows up in an analytics tool as "dark traffic, devoid of referral data, impossible to attribute," not as a credited referral. His own example: over 60% of a site's traffic and sessions came in as direct, with no way to trace which upstream mention caused it. His fix is directional, not precise — watch branded search, direct traffic, and conversions as trend lines over months, and accept "correlation does not imply causation (though it sure can be a hint)" as the honest ceiling on channel measurement. ([SparkToro, "How to Measure 'Hard-to-Measure' Marketing Channels"](https://sparktoro.com/blog/how-to-measure-hard-to-measure-marketing-channels/))

None of this replaces a real controlled experiment where one is possible. Reach for a quasi-experiment only when randomizing genuinely isn't an option.
