---
name: mk-measurement
description: "This skill should be used when the user asks what to measure, whether marketing is working, how to set up a channel experiment, what belongs on a marketing dashboard, or how to read the results of a launch or campaign."
---

## Purpose

"Is marketing working" only has an honest answer once three things are fixed: which funnel stage a number actually belongs to, what kind of question is being asked of it, and whether the way it was collected can be trusted. This skill builds the scorecard, sets up the experiment, and reads the result — it doesn't run the campaign itself.

## When to use

What to measure, whether marketing is working, setting up a channel experiment, what belongs on a dashboard, or reading the results of a launch or campaign.

## Workflow

1. **Put every metric on a funnel stage.** [The funnel-KPI map](references/funnel-kpi-map.md) uses Dave McClure's AARRR stages — Acquisition, Activation, Retention, Referral, Revenue — from his "Startup Metrics for Pirates" slides, as the shared vocabulary. For each stage a scorecard tracks, give the metric a formula anyone could recompute by hand, a source of truth, and a "something's wrong" trigger. Don't invent a metric for a stage that doesn't apply yet — a pre-revenue product has nothing honest to put in Revenue, and that's fine.
2. **Route the question before answering it.** [The question router](references/question-router.md) sorts a measurement question into descriptive (what happened), diagnostic (why), predictive (what will happen), or prescriptive (what to do) — from Gartner's analytics maturity model — and only a diagnostic answer should justify a prescriptive one. Once the type of question is settled, match it to a chart using the same reference's sourced chart-selection rules, rather than defaulting to whatever chart type is already on the dashboard.
3. **Read reach metrics per platform, not as one number.** [Reach metrics](references/reach-metrics.md) covers what LinkedIn, YouTube, and X each actually define and report — impressions, unique reach, click-through rate, engagement rate — sourced from each platform's own help documentation. These aren't interchangeable across platforms, and impressions alone say more about existing audience size than about anything new the content reached.
4. **Build trustworthy experiments, and know when you can't.** [Trustworthy experiments](references/trustworthy-experiments.md) covers fixing sample size before looking at data, the ways a "significant" result still misleads (sample ratio mismatch, short-term movement that reverses, and the twelve metric-interpretation pitfalls from Dmitriev et al.'s KDD paper), and what to do when there's no control group at all — difference-in-differences, synthetic control, and the honest limits of channel-level attribution.
5. **Build the deliverables** from [scorecard.md](templates/scorecard.md), [experiment-card.md](templates/experiment-card.md), and [monthly-readout.md](templates/monthly-readout.md), each keyed to the AARRR stage and question type it's actually answering.
6. **Route what this skill doesn't own.** The campaign or launch being measured is planned in `mk-launch`, `mk-lifecycle`, `mk-outreach`, or `mk-founder-content`; positioning and audience definitions that a metric is supposed to validate come from `mk-positioning` and `mk-audience`. If the `product-strategy` plugin is installed, `pm-objectives` or `pm-growth` is where a metric ties back to a business goal — this skill measures the number, not what the number should be.

## Outputs

- `scorecard.md` — the standing dashboard, one row per AARRR stage.
- `experiment-card.md` — one experiment: hypothesis, sample size, primary metric, decision rule.
- `monthly-readout.md` — a periodic read of the scorecard, routed through the question types above.

## Adaptable prompt

"Build a scorecard for [product] using AARRR stages, with only the metrics we can actually source today. For [channel or campaign], set up an experiment card with a fixed sample size and one decision rule before we look at any data. When results come in, route the read through descriptive → diagnostic before recommending anything prescriptive."
