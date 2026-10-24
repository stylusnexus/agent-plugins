---
name: pricing-review
description: Review pricing and packaging for a SaaS product - value metric, tier design, willingness-to-pay evidence, a sourced competitor scan, and a grandfathering and migration plan for price changes. Ends in a one-page recommendation. Use when asked to "review pricing", "design tiers", "should we raise prices", or before shipping a pricing change on a product with paying customers.
---

# Pricing Review

## Overview

Pricing changes have a large blast radius. Wrong tiers churn customers, wrong price points leave money on the table, and a botched migration burns trust with the first paying users. This skill produces a one-page recommendation grounded in evidence. No pricing model ships on assumed willingness to pay; it ships on observed or tested willingness to pay, or the recommendation says plainly that the evidence does not exist yet.

If the repository or workspace defines its own `pricing-review` skill, follow that one instead.

Related skills in this marketplace: `pm-value-proposition` for who the customer is and what they value, `pm-discovery` for designing the willingness-to-pay test, `pm-growth` for monetization loops, and `stripe-billing` (in the `ship-pipeline` pack) for implementing the result.

## Workflow

1. **Identify the value metric.** What does the customer pay more for as they get more value? Do not default to "per seat". Ask what scales with the customer's usage and their perceived value.
   - Candidates depend on the product: projects or workspaces hosted, active collaborators, documents processed, AI generations per month, storage.
   - If users bring their own model API keys, model usage is already billed by their provider. Do not charge for it again; price the product itself.
   - Reject metrics that punish engagement (charging per login, per page view). Charge for value delivered, not for using the product.

2. **Gather willingness-to-pay evidence before proposing numbers.** Check what already exists:
   - Billing data (Stripe or similar): free-to-paid conversion, upgrade and downgrade frequency, churn by tier, average revenue per account.
   - Product analytics: drop-off at the pricing page, results of any pricing experiment already run.
   - Support history: has anyone said "I'd pay for X" or "too expensive for Y"? A `customer-support-triage` skill, if installed, tags these.
   - If none of this exists, you have a guess, not a finding. Say so in the recommendation and propose a validation step first.

3. **Design two to four tiers.** Each tier needs:
   - A name and a one-line "who this is for".
   - The value-metric limits at that tier, as concrete numbers, not "generous".
   - A clear reason to upgrade to the next tier: a feature or limit the customer will actually hit.
   - Anti-pattern check: a tier that is a strict subset of another with only a price difference is a discount, not a tier.

4. **Run a competitor pricing scan** with current sources. Search for each competitor's pricing page now; pricing pages change often and memory is stale. Record the value metric and price anchor, not just the sticker price, and link each source. A competitor with "contact us" pricing is recorded as unknown, never guessed.

5. **If this is a price change, write the grandfathering and migration plan explicitly:**
   - Existing customers: grandfathered indefinitely, grandfathered for N months, or migrated with notice?
   - Notice period and the exact email and in-app touch points.
   - Stripe mechanics: a Price's amount cannot be changed after creation. Create a new Price, point new signups at it, and archive the old one (`active=false`). Archiving does not affect existing subscriptions; they stay on the old Price until you move them. Archiving does deactivate existing Payment Links that use the old Price, so recreate those on the new one. A `lookup_key` moved with `transfer_lookup_key=true` lets the pricing page pick up the new Price without a code change. Source: [Stripe, Manage products and prices](https://docs.stripe.com/products-prices/manage-prices). Moving an existing subscription to a new Price raises proration questions; see [Stripe, Prorations](https://docs.stripe.com/billing/subscriptions/prorations).
   - Downgrade path: what happens to a customer's data if they do not upgrade and are now over a new, lower limit? Never silently delete. Degrade gracefully: read-only, capped, or grandfathered on that resource.
   - Refund and terms wording must not contradict the migration promises. A `legal-docs` skill, if installed, covers the refund policy text.

6. **Write the one-page recommendation:**
   - **Value metric:** what and why.
   - **Proposed tiers:** a table of tier name, price, limits, and target customer.
   - **Evidence:** what supports this, or "no evidence yet; run this experiment first".
   - **Competitor anchor:** two or three comparable price points with source links.
   - **Migration plan:** grandfathering terms, notice period, Stripe steps (for a change).
   - **Risks:** the likely churn scenario and the limit most likely to generate support complaints.

## Early-stage price rules

For a young subscription product with few customers, apply these checks to the draft recommendation. They are heuristics from bootstrapped-SaaS practice (see Arvid Kahl, *Zero to Sold*, 2020), not laws; state when evidence says otherwise.

- **With zero customers, lean higher.** No sales at a low price equals no sales at a high price, and a later increase is harder than a later discount. A low price also tells buyers the product is minor.
- **Offer a yearly plan from launch.** Discounted, non-refundable with a visible policy, with room for hardship exceptions. It brings cash forward and shows who is committed.
- **Treat free tiers and lifetime plans as modeled bets.** Before offering either, estimate cost per user and what happens if users grow tenfold. Define "lifetime" in the terms, and review lifetime sales as a one-off cash boost, not recurring revenue.
- **Retire a plan with notice.** Choose upgrade or time-limited grandfathering, and announce at least a few weeks ahead, preferably a month or more. Indefinite grandfathering blocks expansion revenue.
- **Check the base.** With only a handful of customers, one cancellation can remove a large share of revenue. Say so in the Risks section rather than extrapolating from a small base.

## Worked example

A team-notes app has 300 paying teams on a single $12 per seat plan and wants tiers.

- **Value metric:** seats track value poorly; teams with many read-only members churn. Shared workspaces with active editors track value better. Recommendation: price on active editors; viewers are free.
- **Evidence:** billing data shows 40% of seats never edit; three support tickets in the last quarter say "we can't justify paying for people who only read". No pricing experiment has run, so price points are flagged as untested.
- **Tiers:** Free (1 workspace, 3 editors), Team ($8 per editor, unlimited workspaces, version history), Business ($15 per editor, SSO, audit log). The upgrade reason from Team to Business is SSO, which the support log shows larger customers ask for.
- **Competitor anchor:** two competitors' current pricing pages, linked, both priced per member; one offers free viewers.
- **Migration:** existing teams keep $12 per seat for 12 months, then move to Team with 60 days' notice. New Stripe Prices are created for Team and Business; the old Price is archived so no new signups land on it; existing subscriptions are moved at renewal.
- **Risk:** teams with many editors pay more under per-editor pricing. The recommendation lists the 15 accounts affected and suggests a goodwill cap for them, as a decision for the owner.

## Checklist

- [ ] Value metric identified and justified, not copied from a competitor
- [ ] Willingness-to-pay evidence gathered, or the gap stated plainly
- [ ] Two to four tiers, each with a real differentiator
- [ ] Competitor scan from current, linked sources
- [ ] Grandfathering and migration plan written for any change to existing pricing
- [ ] Stripe plan uses new Prices and archives old ones; existing Prices are never treated as editable
- [ ] One-page recommendation format followed

## Output

A single markdown recommendation covering the six parts above. If it is committed, put it in the project's planning or docs folder, not in live app code.

## Stop conditions

- No willingness-to-pay evidence exists at all: say so and recommend a validation step before proposing prices. Do not present a guess as a finding.
- The change affects active paying subscribers: do not finalize the migration plan without explicit sign-off from whoever owns pricing decisions. It touches real customer billing.
- Competitor pricing cannot be found or is "contact us": record it as unknown rather than guessing a number.
