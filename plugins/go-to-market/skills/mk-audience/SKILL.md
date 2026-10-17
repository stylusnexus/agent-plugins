---
name: mk-audience
description: "This skill should be used when the user asks who the first customer is, who to target, an ideal customer profile, buyer personas, who influences the buyer, where an audience gathers online, or how to segment customers."
---

## Purpose

Before a positioning or a plan is any good, someone has to be right about who it's for — a real account or person, built from evidence, not a guessed persona. This skill defines that audience: an ideal customer profile, whether and how to split it into segments, who else shapes the buying decision, where that audience already gathers, and what happens to a contact once they've found the product.

## When to use

Use this when someone asks who the first customer is, who to target next, what an ideal customer profile looks like for this product, whether to segment at all and by what, who besides the buyer needs convincing, or where an audience already spends time online.

## Workflow

1. **Build the profile from evidence, not a guess.** Combine firmographic/technographic/behavioral criteria with Jobs to Be Done — the job the buyer is hiring the product for, not just their job title. Mark every field `MISSING INFORMATION` until it has a real source: a conversation, a support thread, a forum post in the customer's own words. See [icp.md](references/icp.md).
2. **Decide whether — and how — to segment.** Check which base the evidence actually supports (geographic, demographic, psychographic, behavioral, or the B2B-specific firmographic/technographic/needs-based bases), then size each candidate segment against a reachability and distinctness bar before keeping it — segmenting past what the evidence supports adds cost without adding insight. See [segmentation-questions.md](references/segmentation-questions.md).
3. **Name who else is in the room.** The person who signs off is rarely the only one whose opinion mattered — an initiator, a day-to-day user, a technical influencer, a decider, a gatekeeper can all be different people on one purchase. Identify these roles per target rather than assuming a fixed committee every time; a solo-buyer purchase can genuinely be one person's call. See [buying-centre.md](references/buying-centre.md).
4. **Find where this audience already gathers.** Dispatch the `audience-scout` agent to verify real, active, fetched places rather than guessing at a subreddit or a Discord; hand verified places to `mk-community` for how to participate in them.
5. **Name the states a contact moves through** once they've signed up or shown up — enters, moves forward, stalls, or comes back — so a waitlist or signup flow can actually be managed. See [contact-paths.md](references/contact-paths.md).
6. **Fill the [ICP template](templates/icp-template.md).**

Revisit this when a new segment or signup shows up unprompted in real customers, or before a positioning decision that depends on it — an audience definition drifts as real customers accumulate, it isn't a one-time exercise.

## Routing

- `mk-positioning` — once the segment is settled, to pick the alternative and category that fits it.
- `mk-outreach` — for reaching a named person or account directly, including a warm introduction through someone in the buying centre.
- `mk-community` — for participating in a place `audience-scout` found, rather than posting cold into it.
- `marketing-lead` — for the larger plan this audience feeds into.

## Outputs

A filled [ICP template](templates/icp-template.md) with each field sourced or marked `MISSING INFORMATION`/`ASSUMPTION`, a segmentation decision with the rejected bases named, a short list of buying-centre roles per target, and — from `audience-scout` — a verified table of real places this audience gathers.

## Adaptable prompt

"Here's what [PRODUCT] does and who's bought or signed up so far: [real evidence]. Build an ideal customer profile from that evidence only, decide whether it's worth segmenting and by what, name who else besides the buyer is likely involved in the decision, and tell me where to find more people like them — mark anything without a real source as `MISSING INFORMATION`."
