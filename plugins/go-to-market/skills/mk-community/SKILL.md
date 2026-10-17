---
name: mk-community
description: "This skill should be used when the user asks about Discord servers, subreddits, forums, open-source community building, GitHub issues and discussions as marketing, or participating in a hobby, enthusiast, or developer community."
---

Showing up as a genuine member of a community — a subreddit, a Discord server, a forum, a hobby or enthusiast space, or an open-source project's own README/issues/docs — where promotion is the smallest, least frequent part of the work. This is public, ongoing participation, distinct from a 1:1 message to a named person (`mk-outreach`).

## When to use this skill

Planning or reviewing participation in a specific online community: what to post, whether a post fits a community's rules, how to build presence in a hobby or developer space, or how to run an open-source project's community surface.

## Workflow

1. **Identify the kind of community.** A hobby or enthusiast space (forums, Discord, subreddits, marketplace/portfolio sites — see [hobby-community.md](references/hobby-community.md)) and a developer/open-source audience (the repo itself, its issue tracker, its docs — see [opensource-community.md](references/opensource-community.md)) reward different kinds of contribution and don't map onto the same playbook.

2. **Fetch that specific community's current rules before drafting anything.** Community and self-promotion rules live at the level of the individual subreddit, server, or forum, not the platform as a whole, and they drift. Follow [platform-rules-protocol.md](references/platform-rules-protocol.md): fetch the rule, record the exact URL and fetch date in the [participation log](templates/community-participation-log.md), and default to the most conservative reading if a rule can't be found.

3. **Participate before promoting.** Spend most community time on genuine participation — answering questions, trying and crediting other people's work, actually fixing what gets reported — and cap marketing-specific effort at a small, sustainable share of it. A team that only ever shows up to post its own link reads as spam even inside its own rate limit.

4. **For an open-source project, treat the repository itself as the community surface.** The README should answer what the project does, why it's useful, and how to get started; a CONTRIBUTING file and a few newcomer-labeled issues lower the bar to a first contribution; and a fast first reply (even just a thank-you and a review date) keeps people from assuming they've been ignored. Only call something "open source" if its license actually meets the Open Source Definition — see [opensource-community.md](references/opensource-community.md) for what that requires and for real, named small projects doing pieces of this well.

5. **Run it as a wheel, not a funnel.** Per [inbound-flywheel-for-community.md](references/inbound-flywheel-for-community.md): attract (genuine participation), engage (following through on replies and fixes), and delight (closing the loop well enough that someone tells another person, unprompted) feed each other in a cycle — a community that's only ever asked of, never given to, is friction that slows the cycle down rather than feeding it.

6. **Review the log for health, not just cadence.** A give:ask ratio that stays high, and any real signs of delight (unprompted mentions, contributors returning, people bringing others in), matter more than whether a post went out on schedule.

## Routing to sibling skills

- `mk-founder-content` — for the devlog, process, or update posts that fuel genuine participation in a community.
- `mk-audience` — to confirm which specific communities the target audience is actually in before spending time in the wrong one.
- `mk-outreach` — when the right move is a message to one named person, not a public post.
- `mk-measurement` — for tracking community health (response time, contributor return rate) over vanity metrics like stars or follower counts.
- `marketing-lead` — for how community time fits the team's broader, hours-bounded plan.

## Outputs

A filled [community participation log](templates/community-participation-log.md) entry, including the fetched rule URL and date. A go/no-go read on whether a specific draft post fits a specific community's current rules. For open-source work, a checklist of what the repo itself is missing (README, CONTRIBUTING, labeled issues, response-time commitment).

## Adaptable prompt

"I want to participate in [specific subreddit / Discord server / forum / open-source repo's community]. Fetch its current rules first and record the URL and date. Then tell me: is [draft post or plan] a fit for this specific community right now, and what should I do first (participate, review, answer something) before posting anything promotional?"
