# The North Star metric: choosing, defining and retiring one

Concept grounded in "One Metric That Matters" from Alistair Croll & Benjamin Yoskovitz,
*Lean Analytics* (O'Reilly, 2013; [overview](https://medium.com/lean-stack/lean-analytics-the-one-metric-that-matters-and-other-provocations-fd3006aab17)) and Amplitude's public North Star Framework
material (amplitude.com/north-star). Treat both as shared vocabulary for the same idea — a
single number tracking the value customers get — not one canonical spec.

## What it is and isn't

A North Star metric is a bet, not a fact: the hypothesis that if this number rises, customers
are getting more real value and the business benefits downstream. It earns its place only while
that bet keeps paying off in evidence. It is not an OKR (an OKR can use it as a key result), not
a KPI dashboard, and not a replacement for strategy. A product with several distinct jobs may
need several North Stars, or none yet, rather than one metric stretched to cover unrelated value.

## Define it completely or don't use it

An undefined North Star is a slogan. Pin down: the qualifying event (precise enough that two
people tag the same raw data the same way), the eligible population, the time window and unit,
the exact formula and data source, and the owner plus deliberate exclusions (bots, test
accounts, refunds).

## Choosing a candidate

Screen options against: does it sit close to the value customers actually came for, rather than
something merely correlated with it (page views and login streaks move easily without anyone
getting more value)? Can the team credibly move it through decisions it owns? Is it hard to game
without also creating real value? Does everyone compute it the same way? What does it
deliberately leave out? Compare two or three candidates against these questions side by side
before committing — the comparison teaches more than any single score.

## The supporting tree and its guardrails

List the small number of input metrics a team can actually influence and plausibly drives the
North Star, stating the *mechanism* for each link, not just a correlation — and treat every
mechanism as untested until checked against real cohort data or a live experiment. Prune inputs
that don't actually move the number.

Pair the North Star with one or two guardrails before launch — typically retention, quality,
support load, or trust — that would flag harm the North Star itself wouldn't show. Decide in
advance what a guardrail breach triggers; deciding that under pressure tends to favor keeping
the number climbing.

## Where it plugs in

Strategy names the value it's betting on; `pm-objectives` treats it as a candidate key result,
not the only one; roadmap uses it as a prioritization lens, not a scorecard; discovery keeps
testing whether it still tracks value. Don't introduce a North Star to look rigorous when the
value proposition or the data to measure it is still unclear.

## Retiring it

A North Star stops earning its place when the mechanism linking it to value breaks (pricing
change, new segment, a feature that makes the old proxy meaningless) or when it can be
satisfied without the customer benefiting. Revisit it on a fixed cadence, not only once it's
visibly broken.

## Tooling

Use pm-visuals (Lucid where connected, Mermaid otherwise) to diagram the North Star and its
input tree alongside the written definition. The plugin's `scripts/metrics_lookup.py`, backed
by [the metric reference](metrics-catalog.md), helps pull a candidate definition to adapt — it
doesn't choose a North Star, compute a live value, or validate a causal link. Read the host
analytics skill before requesting any authorized data pull.
