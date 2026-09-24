---
name: mk-lifecycle
description: "This skill should be used when the user asks for a waitlist sequence, onboarding emails, an activation email flow, a win-back or upgrade email, a lifecycle map, or how to nurture signups toward paying."
---

## Purpose

Lifecycle email works on two things this skill keeps separate: knowing where a contact actually is (a stage, moved by something real they did) and knowing what to say to move them forward (drafted in the product's own voice, judged by signals a send can actually tell you). It builds the map and the sequences; it routes the actual copywriting craft to `mk-copy` and the segment-finding survey to whoever owns the product relationship.

## When to use

A waitlist sequence, onboarding or activation emails, a win-back or upgrade email, a lifecycle map, or a plan for nurturing signups toward paying.

## Workflow

1. **Name the stages before writing any email.** [Lifecycle stages](references/lifecycle-stages.md) covers HubSpot's own definition and default set (Subscriber, Lead, Marketing Qualified Lead, Sales Qualified Lead, Opportunity, Customer, Evangelist, Other) — most small teams only need two or three of these until the rest become real distinctions. The key mechanic: HubSpot's own stage property moves forward automatically and never backward on its own; a stage nobody can actually detect isn't a stage yet, and disengagement is a separate signal (a status field, an unsubscribe, a churn flag), not a lifecycle-stage reversal.
2. **Find who the product actually works for before designing onboarding.** [The core-segment survey](references/pmf-segment-survey.md) — grounded in Sean Ellis's method and Rahul Vohra's public account of running it at Superhuman — asks active users "how would you feel if you could no longer use [product]," and segments the "very disappointed" answers into personas. That persona's specific reason for loving the product becomes onboarding's actual target, not a generic "aha moment." Only survey people who've used the product; a cohort that hasn't earns a welcome email and, at most, one question about intent.
3. **Draft in the product's own voice, not a list of adjectives.** Hard rule for every email: never invent a product capability, a person's stated reason, a result, or "we've talked to X" evidence — check every sentence against a supplied fact and label a single self-reported result as self-reported, not verified (see `marketing-lead/references/principles.md`). [Brand voice and the email loop](references/brand-voice-email-loop.md) covers pulling real sentences the product has already said in public (a README line, pricing copy, a founder's own phrasing) and drafting toward that register — and, once sends go out, what open rate can and can't tell you now that Apple's Mail Privacy Protection pre-loads the tracking pixel on delivery regardless of whether anyone opens the email. Build the read on clicks, conversions, replies, and unsubscribes; treat open rate as context, not the headline number.
4. **Build the map and the sequence** from [lifecycle-map.md](templates/lifecycle-map.md) and [onboarding-sequence.md](templates/onboarding-sequence.md), using only stages the team can actually observe and triggers tied to real behavior, not a fixed day-count.
5. **Route what this skill doesn't own.** The actual email copy and subject lines get drafted and pre-publish-checked in `mk-copy`; who the segment is and how to reach them for the survey comes from `mk-audience`; the product's messaging comes from `mk-positioning`; results (click rate, conversion, a pattern across two or three sends, not one) get read in `mk-measurement`. If the `product-strategy` plugin is installed, `pm-growth` or `pm-objectives` is where "nurture toward paying" ties back to a revenue target — this skill assumes that target already exists.

## Outputs

- `lifecycle-map.md` — the stages, the trigger into and out of each, and what's currently undetectable.
- `onboarding-sequence.md` — the triggered sequence itself, keyed to real behavior.

## Adaptable prompt

"Map [product]'s lifecycle stages using only signals we can actually detect today, then draft an onboarding sequence triggered by real behavior (not a fixed day-count) aimed at the specific 'aha' moment from [persona]'s very-disappointed survey answers. Draft in [product]'s own voice from these examples: [paste real copy]. Flag anything that needs a subject-line or copy pass from mk-copy."
