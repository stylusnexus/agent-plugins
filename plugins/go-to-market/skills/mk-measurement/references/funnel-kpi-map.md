# Funnel KPI map

Every metric on a scorecard should trace to a stage of the funnel it's measuring. This reference maps common funnel stages to the KPIs that actually belong to them, so a scorecard doesn't end up with five metrics that all describe the same stage while others go unwatched.

## The stages

Dave McClure's "Startup Metrics for Pirates" framework (often shortened to AARRR after its five stages) is the most widely reused funnel shape in startup marketing, and its stage definitions are still a useful vocabulary even when the specific tactics in the original slides have aged. From McClure's own slides ([Startup Metrics for Pirates](https://www.slideshare.net/dmc500hats/startup-metrics-for-pirates-long-version)):

- **Acquisition** — "Users come to the site from various channels." What to watch: visits or signups by channel, and the cost or effort per channel, so spend follows what actually brings people rather than what feels highest-effort.
- **Activation** — "Users enjoy 1st visit: 'happy' user experience." What to watch: whether a new signup reaches the product's real first win, not just whether they created an account — McClure's own thresholds (page views, time on site) are dated, but the principle of picking a concrete "happened or didn't" moment still holds.
- **Retention** — "Users come back, visit site multiple times." What to watch: whether people who activated are still active weeks later, tracked as a cohort over time rather than a single daily-active count.
- **Referral** — "Users like product enough to refer others" — and McClure is explicit that this only works "after they have 'happy' user experience." What to watch: whether activated, retained users refer anyone, not whether a referral button exists.
- **Revenue** — "Users conduct some monetization behavior." What to watch: whichever monetization event the specific business actually has (trial-to-paid conversion, upgrade rate).

## A second lens: reach before conversion

Rand Fishkin's SparkToro three-tier funnel (see [trustworthy experiments](trustworthy-experiments.md#quasi-experiments-when-you-cant-randomize) for the full sourcing) is a useful check on the AARRR stages above it, because it separates awareness that never gets attributed from the acquisition numbers a dashboard can actually count. Per SparkToro's own tiers: **top of funnel** is "people that haven't yet reached your website" — social impressions and new followers, and brand mentions on channels like podcasts or Reddit that never get attributed. **Middle of funnel** is direct ("type-in") traffic and branded-keyword search — "more than 60% of users and sessions come direct" on SparkToro's own site — plus subscriber growth. **Bottom of funnel** is "conversions. Email signups. Free trials. Logins. Purchases" — where AARRR's Acquisition stage begins. Source: SparkToro, "How to Measure 'Hard-to-Measure' Marketing Channels" — https://sparktoro.com/blog/how-to-measure-hard-to-measure-marketing-channels/. A scorecard that only tracks AARRR's stages can miss a channel that's building the top or middle of this funnel — brand awareness that hasn't converted yet — and read it as doing nothing.

## Putting a KPI on each stage

For each stage a scorecard tracks, give the metric three things: a formula that anyone on the team could recompute by hand, a source of truth (which system actually holds this number), and a "something's wrong" trigger — the movement that means look now, not at the next monthly readout. A metric without a trigger just sits on the page; a metric without a formula gets redefined differently by whoever pulls it next.

Don't put a KPI on a stage just because the stage exists. A pre-launch product with no revenue yet has nothing honest to put in the Revenue row — mark it not yet applicable rather than inventing a proxy number to fill the space.
