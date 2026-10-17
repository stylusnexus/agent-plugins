---
name: feature-flags
description: Feature-flag lifecycle, using PostHog as the worked backend - naming, deciding rollout flag versus kill switch, staged rollout percentages, wiring kill switches to an alert, testing both code paths, and a stale-flag cleanup pass that removes code before disabling the flag. Use when asked to "add a feature flag", "roll out a feature gradually", "add a kill switch", or "clean up old flags".
---

# Feature Flags

## Overview

Flags serve two purposes: progressive rollout (de-risking a launch) and kill switches (turning a risky path off without a deploy). Both decay into flag debt if nobody cleans them up. This skill covers the whole lifecycle: creation, rollout, testing, and the cleanup pass most teams skip.

PostHog is the worked example. The lifecycle applies to any flag service (LaunchDarkly, Unleash, GrowthBook, a config table); swap in its equivalents. If the repository defines its own `feature-flags` skill or flag conventions, follow those instead.

## Naming

Kebab-case, area first, then feature: `billing-annual-plan-prompt`, `editor-ai-summary`. Avoid generic names (`new-feature`, `test-flag`); six months later nobody remembers what `test-flag` gates. Prefix kill-switch flags with `kill-` so their purpose shows in the flag list without opening each one: `kill-ai-summary-generation`. If the repository already has a naming convention, match it.

## Workflow

1. **Decide the flag's purpose before creating it:**
   - **Rollout flag:** temporary. It is removed once it is at 100% and stable, and it gets a planned removal date on day one.
   - **Kill switch:** long-lived. It guards a specific risky path (an external API call, expensive AI generation, a new payment flow) so it can be turned off instantly. It stays as long as the guarded code exists.
   - Do not mix the two. A rollout flag that quietly becomes a permanent kill switch is how flag debt starts.

2. **Start the rollout low.** A typical progression is 5% → 25% → 50% → 100%, holding each step for at least 24 to 48 hours when the feature has real usage, and longer when it affects billing or paid-API costs; those need more signal before the next step. A low-risk cosmetic change can go 25% → 100%. Anything touching payments, user data, or stored credentials never skips the low-percentage soak.

3. **Wire each kill switch to something observable.** A switch nobody knows to flip is not wired. Pair it with:
   - An alert on the error rate or cost metric it exists to catch (in PostHog, an insight alert; or the project's uptime or error-tracking alerts).
   - A findable runbook line: "if X spikes, turn off flag Y". A code comment beside the flag check or an entry in the on-call notes is enough, as long as someone can find it at 2am.

4. **Test both code paths.** Every flag needs coverage for on and off. A stale `else` branch nobody has run since week one is where regressions hide: the flag gets flipped back during an incident and the "safe" fallback is broken too. In end-to-end tests, parametrize the flag state instead of duplicating test files.

5. **Before going to 100%:** the error rate and cost metric are stable at the current percentage for the full soak window, no open bugs are tied to the feature, and for AI-generation or billing flags, cost per user is not climbing as the percentage rises.

6. **Stale-flag cleanup pass** (monthly, or when asked):
   - List stale flags. PostHog treats a flag as stale when it has not been evaluated in 30 or more days, or has been at 100% rollout with no property filters for 30 or more days; disabled flags do not count. Filter the flag list by status in the app, or call the feature flags API with `active=STALE` and fetch every page. Source: [PostHog, Cleaning up stale feature flags](https://posthog.com/docs/feature-flags/cleaning-up-stale-flags).
   - For each stale rollout flag, **remove the code first**: collapse the flag check to the "on" branch, delete the "off" branch, and deploy. Only then disable the flag. Disabling a flag that code still checks turns the feature off for everyone, even at 100%.
   - Prefer disabling over deleting: disabling keeps the configuration so re-enabling is instant; deleting means recreating it. Delete only a flag you are confident you will never need again, such as an abandoned rollout whose code is already gone.
   - Disabled flags never appear in the stale list, so list them separately (filter the flag list by disabled status). Each is either an abandoned rollout (remove the dead code, then delete the flag) or a parked kill switch (rename it with the `kill-` prefix if needed, and leave it).
   - Open one small cleanup PR per flag, not one PR touching every stale flag. Each is easier to review and to revert if removing a flag exposes an unexpected dependency.

## Worked example

Adding an AI summary feature that calls a paid model API.

- **Flags:** `editor-ai-summary` (rollout flag, removal planned four weeks after reaching 100%) and `kill-ai-summary-generation` (kill switch around the model call).
- **Rollout:** 5% for 48 hours, then 25% for 48 hours, then 50%, then 100%. It is a paid-API feature, so each step waits on the cost chart as well as the error rate.
- **Kill switch wiring:** an alert fires when model spend per hour exceeds twice the 7-day average. The code comment beside the check reads: "If the AI cost alert fires, turn off kill-ai-summary-generation."
- **Tests:** the summary component's end-to-end test runs with `editor-ai-summary` on and off; a unit test confirms the kill switch returns the "summary unavailable" state without calling the API.
- **Cleanup, five weeks later:** `editor-ai-summary` shows as stale (100%, no filters, 30+ days). A PR removes the flag check and the off-branch; after it deploys, the flag is disabled in PostHog. `kill-ai-summary-generation` stays.

## Checklist

- [ ] Flag named per convention; purpose (rollout or kill switch) decided up front
- [ ] Rollout staged, with soak time observed at each step
- [ ] Kill switch wired to an alert, with a findable runbook line
- [ ] Both on and off code paths tested
- [ ] Pre-100% check done: errors, cost, open bugs
- [ ] Cleanup pass: code removed and deployed before the flag is disabled; kill switches kept

## Output

For creation: the flag configuration (name, purpose, rollout stages, kill-switch alert) plus the PR implementing both code paths. For cleanup: a table of stale flags (name, rollout, last evaluated, recommended action) and one PR per flag removed.

## Stop conditions

- A flag guarding a payment or credential-handling path needs to reach 100%: do not skip the soak window under time pressure. Confirm the metric is stable, not just quiet.
- The cleanup pass finds an off flag with no clear owner or history: do not delete it. Ask before removing anything that might be an emergency brake for live code.
- Going to 100% would remove the only rollback path for a feature with recent incidents: hold at the current percentage and ask the feature's owner first.
