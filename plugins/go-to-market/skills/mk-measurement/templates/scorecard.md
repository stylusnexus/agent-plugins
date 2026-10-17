# Marketing scorecard

One row per AARRR stage — see [the funnel-KPI map](../references/funnel-kpi-map.md). Leave a stage's row marked "not yet applicable" rather than inventing a proxy metric for it.

| Stage | Metric | Formula (recomputable by hand) | Source of truth | "Something's wrong" trigger | This period |
|---|---|---|---|---|---|
| Acquisition | | | | | |
| Activation | | | | | |
| Retention | | | | | |
| Referral | | | | | |
| Revenue | | | | | |

## Reach, by platform

Pull only the metrics each platform actually defines — see [reach metrics](../references/reach-metrics.md). Don't blend platforms into one "engagement" number; they don't measure the same thing.

| Platform | Impressions / thumbnail impressions | Unique reach | Click-through rate | Engagement rate |
|---|---|---|---|---|
| LinkedIn | | | | |
| YouTube | | | | |
| X | | | | |

## Before trusting any row

- Is the sample big enough to read anything into, or is this still noise? (See [trustworthy experiments](../references/trustworthy-experiments.md).)
- Does this metric's movement need a diagnostic pass before anyone acts on it? (See [the question router](../references/question-router.md).)

---

## Example (fictional)

| Stage | Metric | Formula | Source of truth | Trigger | This period |
|---|---|---|---|---|---|
| Acquisition | signups by channel | count of new accounts, grouped by UTM source | product database | any channel drops >30% week over week | 212 |
| Revenue | trial-to-paid rate | paid accounts ÷ trials started, 30-day window | billing system | drops below prior 3-month average | not yet applicable — pre-launch |
