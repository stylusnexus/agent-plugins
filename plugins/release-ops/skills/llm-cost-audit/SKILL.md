---
name: llm-cost-audit
description: "Measure and reduce what a product pays for LLM calls - reconcile tracked cost with the provider's bill, check each call site's model tier, find prompt-caching and batch candidates, check that bring-your-own-key paths stay user-paid, and set budget alerts. Ends in a savings table with the cost-per-call arithmetic shown. Use for \"audit our AI spend\", \"why is our model API bill high\", \"reduce LLM costs\", or as a periodic cost-hygiene pass."
---

# LLM Cost Audit

## Overview

Audit spend where the product actually pays the bill, and end with a savings table, not observations. Every price in the audit comes from the provider's pricing page on the day of the audit. Prices, cache multipliers, and discounts change, and they differ between models from the same provider; a number remembered from an earlier audit or a blog post is not evidence.

If the repository defines its own `llm-cost-audit` skill or a model-routing policy, follow that instead.

Pricing pages to read (open them; do not quote from memory):

- Anthropic: [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)
- OpenAI: [developers.openai.com/api/docs/pricing](https://developers.openai.com/api/docs/pricing)
- Google Gemini: [ai.google.dev/gemini-api/docs/pricing](https://ai.google.dev/gemini-api/docs/pricing)
- Any other provider in use: its own pricing page, linked in the report.

## How to compute cost per call

Prices are quoted per million tokens (MTok). For one call:

```
cost = (uncached_input_tokens × input_price
      + cache_write_tokens    × cache_write_price
      + cache_read_tokens     × cache_read_price
      + output_tokens         × output_price) / 1,000,000
```

Take token counts from the API response's usage fields, not from estimates. Multiply cost per call by calls per month (from logs or analytics) to get monthly cost per call site. Some models charge a higher rate per token once a prompt passes a length threshold; check the pricing page for length-based tiers and use the rate that matches each call's prompt length. Apply any discount that applies (batch, regional pricing) as a multiplier stated on the pricing page, and write the page URL and the date read beside every price you use.

## Workflow

1. **Pull current spend from two sources and reconcile them:**
   - **Tracked cost** from LLM observability, for example PostHog LLM analytics (`$ai_generation` events; see [PostHog, Calculating LLM costs](https://posthog.com/docs/llm-analytics/calculating-costs)), Langfuse, Helicone, or the project's own usage table. This shows which *feature* drives spend, not just which model.
   - **Billed usage** from the provider console. Tracked cost drifts from the bill when a call site is not instrumented (a server-side path added without the tracking wrapper). Treat a gap as a bug to fix, not rounding.
   - Break spend down by model, feature or endpoint, and, if the data allows, customer plan. A free-plan feature burning spend out of proportion to what that plan pays is the most common finding.

2. **Check each call site's model tier against the work.** Find every place a model is chosen (search for the provider SDK calls and the `model` parameter). For each:
   - The most capable, most expensive tier belongs only where the work needs it: long-context reasoning, complex multi-step generation, or a task that has failed on a cheaper tier.
   - Routine work (short rewrites, classification, extraction, boilerplate) belongs on a mid or small tier.
   - Use the model IDs and prices on the provider's current pricing and models pages. A top-tier model doing small-tier work is pure margin loss.
   - Flag the reverse too: a call site on a tier too weak for the work is a quality risk. The audit is about routing correctly, not only routing down.

3. **Find prompt-caching candidates:** call sites that send the same long, stable prefix (a system prompt, reference material, a long set of examples) on every request with only the tail changing.
   - Put the stable content first and the variable content after it, so the prefix is cacheable.
   - Estimate savings with the formula above: the cached prefix moves from the input price to the cache-read price, plus occasional cache writes. Read both from the pricing page for the exact model; cache-read pricing differs between models even from one provider ([Anthropic, Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)).
   - Check the provider's minimum cacheable prompt length for that model; a prefix below it is not cached.

4. **Find batch candidates.** Work that needs no synchronous response (nightly generation, bulk classification, backfills, evaluations) can use a batch API. As of this writing both Anthropic and OpenAI document a 50% discount for batch requests, and OpenAI's batches complete within a 24-hour window; confirm the current terms on [Anthropic, Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) and [OpenAI, Batch API](https://developers.openai.com/api/docs/guides/batch). Structure it as submit, poll or receive a webhook on completion, and write results idempotently.

5. **If users bring their own API keys, check the boundary.** Per-user generation is supposed to run on the user's key and bill to their provider account. If the company's own key shows non-trivial spend for that product, either a feature was built without going through the user-key path, or an internal tool uses the shared key for user-scoped work. Flag it; aggregate dollar totals hide this.

6. **Set budget alerts.** If none exist, set a provider-side spend limit or usage alert and an observability alert below the point where spend becomes an urgent conversation (for example at 70% of the monthly budget, not 100%). Pair any feature that can run away (a generation loop with no cap) with a kill switch; a `feature-flags` skill, if installed, covers that. The alert says there is a problem; the switch stops it without a deploy.

7. **Produce the savings table.** This is the deliverable:

   | Finding | Current monthly cost | Action | Estimated savings per month | Price source |
   |---|---|---|---|---|
   | ... | ... | ... | ... | URL, date read |

   End with a total row, and mark which changes are safe to ship now (routing, caching) and which need a test pass first (moving a job to batch changes its structure).

## Worked example

A document app's "summarize" endpoint runs on a provider's top tier.

- **Usage (from the response usage fields, averaged over 30 days):** 6,000 input tokens per call, of which a 5,000-token system prompt and style guide never change; 400 output tokens; 90,000 calls per month.
- **Prices (illustrative, not current; read the real ones from the pricing page):** top tier $5 input and $25 output per MTok; mid tier $2 input and $10 output per MTok, with cache reads at 0.1× input.
- **Current:** (6,000 × 5 + 400 × 25) / 1,000,000 = $0.040 per call, × 90,000 = $3,600 per month.
- **Re-route to mid tier** (a quality check on 50 sampled summaries shows no regression): (6,000 × 2 + 400 × 10) / 1,000,000 = $0.016 per call, $1,440 per month.
- **Then cache the 5,000-token prefix:** (1,000 × 2 + 5,000 × 0.2 + 400 × 10) / 1,000,000 = $0.007 per call, $630 per month, before occasional cache writes.
- **Savings table row:** "Summarize on top tier, uncached | $3,600 | Route to mid tier, cache stable prefix | about $2,970 | pricing page URL, date read".

## Checklist

- [ ] Spend pulled from tracked cost and the provider bill, and the gap explained
- [ ] Every top-tier call site justified, and under-powered call sites flagged
- [ ] Caching candidates estimated with the per-model cache price from the pricing page
- [ ] Batch candidates confirmed to have no hidden latency requirement
- [ ] Bring-your-own-key paths checked for spend leaking onto the company key
- [ ] Budget alert below the urgent point, paired with a kill switch for runaway features
- [ ] Savings table with current cost, action, savings, and a price source per row

## Output

The savings table, plus the per-call-site routing findings (`file:line`) for anything flagged for re-routing.

## Stop conditions

- Tracked cost and the provider bill disagree by more than a small margin: report the tracking gap as the top finding and do not finalize savings estimates on numbers known to be incomplete.
- A price, multiplier, or discount cannot be confirmed on the provider's page today: write "price not confirmed" in that row instead of filling in a remembered number.
- A batch recommendation turns out to block something a user is waiting on: verify the call site is genuinely offline before recommending it.
