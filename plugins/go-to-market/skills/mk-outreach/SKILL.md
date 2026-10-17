---
name: mk-outreach
description: "This skill should be used when the user asks for direct outreach, a cold email, reaching out to press or podcasts, finding design partners, partnership outreach, warm intros, a setup-service offer, or a list of people/companies to contact and what to say to them."
---

Direct, one-to-one outreach: a cold email or LinkedIn message to a named person, a warm introduction through someone the target already trusts, or a hands-on setup-service offer to learn what an early buyer actually needs. This is not community posting (`mk-community`) or a broadcast campaign — every message here is written to one specific, named recipient.

## When to use this skill

Reaching out to a specific person or company: a design partner, a journalist or podcast host, a potential partner, an investor's portfolio contact, or any 1:1 message where the recipient's identity is known in advance.

## Workflow

1. **Confirm the recipient is worth writing to — and worth disqualifying if not.** Outreach is expensive per message — a real ICP or segment (`mk-audience`) and a clear value proposition (`mk-positioning`) should already exist before drafting anything. Outreach without that groundwork is a guess dressed up as a plan. Disqualify before drafting when, for example: no one owns the process this product touches, the company already committed to a competing tool, the integration the pitch leans on isn't one they actually use, or the company is too small/large for the segment this product actually serves. Hard rule for the message itself: never invent a product capability, a person's stated reason for anything, a result, or "we've talked to X" evidence — check every sentence against a supplied fact and label a single self-reported result as self-reported, not verified (see `marketing-lead/references/principles.md`).

2. **Check for a warm path first.** A trusted connector beats a cold message every time — see [warm-intros.md](references/warm-intros.md). Ask the connector, separately, whether they're willing to make the introduction at all, before drafting anything; write the forwardable note yourself, in your own voice, addressed to the target; give the connector an easy out to decline. Only fall back to cold outreach when no real warm path exists — don't stretch a thin connection to manufacture one.

3. **If going cold, get the legal floor right before writing a word of pitch.** See [outreach-method.md](references/outreach-method.md) for what US (CAN-SPAM), EU (GDPR + the ePrivacy Directive), and UK (PECR) recipients each require — honest sender identity, a working opt-out, and (for EU business recipients) checking the destination country's own rule rather than assuming one EU-wide answer. Authenticate the sending domain (SPF/DKIM at minimum) before any volume.

4. **Write to the one recipient, not a template with a name swapped in.** Beyond the legal floor in step 3, the one fixed requirement is at least one specific fact about this recipient that was actually checked, not guessed. Everything else — how the message is worded, structured, and closed — is judgment for that one recipient; there's no fixed formula to fill in.

5. **For an early design partner or first customer, consider offering to do the work by hand instead of pitching a product that doesn't fully exist yet.** See [setup-service-and-buyer-discovery.md](references/setup-service-and-buyer-discovery.md). Do the setup work personally the first few times — that's where real requirements surface — and only generalize a piece of it into a repeatable offer once more than one partner has asked for the same thing.

6. **Track every send and respect every stop signal.** Log one tracker line per send — including each follow-up, not just the first message — so the denominator in any reply-rate math is real sends, not recipients. Honor an opt-out or a clear no immediately; "not now" isn't "never," but it's also not standing consent to keep going indefinitely. When sizing a prospect-count target from a desired number of replies, show the reply-rate assumption behind it explicitly (e.g. "target of 5 replies assumes a 1-in-20 reply rate, so ~100 sends" — label the rate `ASSUMPTION` until a real batch confirms it). Stop rule: after a batch of a few dozen sends with no real interest, stop sending and revisit the audience (`mk-audience`) or positioning (`mk-positioning`) before writing more messages — a low reply rate is a targeting or message problem to diagnose, not a volume problem to push through.

## Routing to sibling skills

- `mk-audience` — before writing anything, to confirm who's actually worth contacting.
- `mk-positioning` — for the value proposition the message leans on.
- `mk-community` — when the right move is showing up in a public space the target already reads, not a 1:1 message.
- `mk-measurement` — to track reply rates and outcomes honestly, with a real denominator.
- `marketing-lead` — for how this outreach motion fits the team's broader, hours-bounded plan.

## Outputs

A draft cold message or forwardable warm-intro note, ready for the owner's review — drafting is never sending (see `marketing-lead/references/principles.md`: plans are not permission). A filled [outreach tracker](templates/outreach-tracker.md) log. A filled [design-partner invitation](templates/design-partner-invitation.md) when the ask includes a hands-on setup offer.

## Adaptable prompt

"Draft a [cold email / LinkedIn message / forwardable warm-intro note] to [name, role, company], about [what we're offering or asking]. The one specific fact I know about them is: [fact — must be real and checked, not guessed]. Recipient is based in [country, for the legal-floor check]. Keep it short, disclose who's writing and why, and end with an ask they can answer either way. Don't send it — just draft it for my review."
