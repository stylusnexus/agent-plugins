---
name: mk-launch
description: "This skill should be used when the user asks for a launch plan, a relaunch plan, help with a Show HN post, a Product Hunt launch, release-day marketing, how to announce a new version, or a launch-day checklist."
---

## Purpose

A launch is one day (or one post) that a lot of other work has to be ready for before it happens. This skill turns "we're launching Thursday" into a plan: which platform(s) actually fit what's shipping, what each platform's current self-promotion and format rules require, what has to be checked across the product before a stranger arrives, and what gets measured once the launch is live. It does not write the announcement copy itself or decide who the audience is — it routes those to the skills that own them.

## When to use

A launch plan, a relaunch plan, a Show HN or Product Hunt submission, release-day marketing for a new version, or a launch-day checklist.

## Workflow

1. **Confirm what's actually shipping.** A launch post has to point at something a stranger can use today — a real build, not a landing page or waitlist. Get this straight before picking a platform. Hard rule for launch copy: never invent a product capability, a person's stated reason, a result, or "we've talked to X" evidence — check every sentence against a supplied fact and label a single self-reported result as self-reported, not verified (see `marketing-lead/references/principles.md`).
2. **Run the touchpoint audit.** Before the announcement goes anywhere, check the places a first-time visitor actually lands — landing page, README, onboarding, empty states, error messages, the signup email, pricing, the support path, the changelog — against [the touchpoint audit](references/touchpoint-audit.md). A launch that nails the headline and skips this fails real visitors, not a hypothetical.
3. **Pick the platform and re-fetch its current rules.** [Platform rules](references/platform-rules.md) covers Show HN, Product Hunt, Reddit, and dev-tool READMEs as a snapshot from one research pass — self-promotion and format rules change without notice, so re-fetch the live guidelines page before relying on any of it for a real launch. Reddit in particular has no single sitewide numeric rule; the subreddit's own posted rules always win.
4. **Build the launch-day checklist and the launch plan** from [launch-day-checklist.md](templates/launch-day-checklist.md) and [launch-plan.md](templates/launch-plan.md), grounded in what steps 2 and 3 turned up.
5. **Route the pieces this skill doesn't own.** Who the launch is for comes from `mk-audience`; the message comes from `mk-positioning`; the actual announcement, README opening, and comment copy get drafted and pre-publish-checked in `mk-copy`; day-one and follow-up email go through `mk-lifecycle`; where else to show up (a community that isn't just a launch platform) goes through `mk-community`. If the `product-strategy` plugin is installed, `pm-roadmap` or `pm-objectives` is the place to confirm launch timing actually fits the plan — this skill assumes that call has already been made.
6. **After launch, measure it.** Hand the AARRR-stage numbers this launch is expected to move to `mk-measurement`, and write [the post-launch readout](templates/post-launch-readout.md) once real data exists — not before.

## Outputs

- `launch-plan.md` — platform choice, readiness gate, day-of sequence, and owners.
- `launch-day-checklist.md` — the day-of checklist itself.
- `post-launch-readout.md` — what actually happened, filled in after the fact.

## Adaptable prompt

"We're launching [product] on [platform(s)] on [date]. Re-fetch that platform's current self-promotion and submission rules, run the touchpoint audit against [landing page / README / onboarding / support path], and build a launch-day checklist and launch plan. Flag anything not actually ready before treating this as go."
