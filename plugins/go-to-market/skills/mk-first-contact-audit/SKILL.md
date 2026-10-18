---
name: mk-first-contact-audit
description: "This skill should be used when the user asks why nobody is using their product, whether a landing page or README makes sense to a stranger, why visitors leave, whether people trust the site, why it is not found or shared well, or wants a diagnosis of a page before any copy is rewritten."
---

## Purpose

When people do not use a product, the cause is rarely one thing. A stranger may not understand it, may not see why it is for them, may not see proof, may not trust the people behind it, may hit a confusing button, or may never reach the page. Each cause has a different fix and a different owner. This skill finds which ones are real, on one page, and routes each fix to the skill that owns it. It writes no copy itself.

## When to use

Use this when someone asks why a product is not getting traction, or wants a page checked as a stranger would see it, before spending time on copy, a launch or a channel. If the ask is a single fix with a known cause (write this headline, plan this launch), go straight to the skill that owns it.

## Workflow

1. **Write the truth down first.** Ask for the one-line truth (what it is, for whom, the problem it solves), the one intended first visitor, and the one action a visitor should take. Keep these from every reader. If the owner cannot give the one-liner, stop and use `mk-positioning`: that is a positioning gap, not a page problem. See [the staged protocol](references/staged-protocol.md).
2. **Collect the mechanical evidence.** Run `python3 scripts/static_signals.py <url>`. It makes one read-only request and reports title, meta description, Open Graph tags, canonical link, JSON-LD, headline, video and caption counts, and whether the raw HTML is a script shell. If it cannot run, fetch the raw HTML with the host's web tool and read the same signals by hand. If a browser is available, also capture the rendered title, headline, visible text and screenshots; otherwise mark rendered findings `NOT VERIFIED`. Never click "Sign in", join a waitlist, or create an account.
3. **Run the staged cold read.** Send each stage's slice (stage 1: URL, tab title, headline; stage 2: first screen; stage 3: whole page; plus the raw HTML for a machine view) to its own fresh `cold-reader` run. Without the agent, follow [the brief](references/cold-reader-brief.md) yourself, one stage per fresh context. Do not tell any reader the category, the audience, or the truth.
4. **Score in a separate step.** Compare each answer to the truth. Score differentiation recall and time to confidence, and flag any confidence below 70. Do not score whether the category guess was right: an AI reader recognizes categories far faster than a person. Use it to find problems and use people to grade them.
5. **Run the checks in order** using [the checks](references/checks.md): a problem worth solving, name and URL, comprehension, relevance, claim typing, proof, trust (six sub-checks), access, machine legibility, model fit. The first failing class gates the fixes. Tag every finding `mechanical`, `multi-reader`, `single-reader`, `LLM-only` or `voices-disagree`.
6. **Offer the human test.** Five people from the audience, ten seconds on the first screen, three questions, using the default pass bar in the protocol. The pass bar is the owner's to set; the default is a proposal with no statistical basis. Drafting the ask to testers is outreach, so hand it to `mk-outreach` and let the owner send it.
7. **Write the scorecard and stop.** Fill [the scorecard](templates/scorecard.md): every check with a quoted line as evidence, at most five fixes ranked with the earliest failing class first, each routed to an owning skill. Only `mechanical`, `multi-reader` and `voices-disagree` findings may rank; the rest are hypotheses with the cheapest check that would settle them.

## Routing

- `mk-positioning` — the one-liner is unsettled, or the audience is unclear.
- `mk-audience` — nobody can say who the first visitor is.
- `mk-copy` — headline, outcomes, proof, call to action, trust wording.
- `mk-brand-kit` — a name that reads badly or a lockup that needs a pronunciation hint.
- `mk-search` — the raw HTML is a shell, or titles and descriptions say little.
- `mk-launch`, `mk-lifecycle` — a launch asset is the real gap, or the steps after sign-up are.
- `mk-measurement` — choosing the one metric that shows whether a fix worked.
- `pm-discovery`, `pm-strategy-fit`, `pricing-review` (`product-strategy` plugin) and `privacy-audit`, `legal-docs` (`hardening` plugin) — when installed. If one is absent, the checks reference says what to write instead.
- `marketing-lead` — the plan the fixes feed into.

## Outputs

A filled scorecard, at most five ranked fixes with routes, a list of hypotheses to verify, and any open question only the owner can answer. Nothing is posted, sent, signed up for or contacted: no reader clicks through, and a plan or scorecard is never permission to publish.

## Adaptable prompt

"Audit [URL] as a stranger would see it. Here is the one-line truth, the intended first visitor and the action we want: [truth], [visitor], [action]. Run the staged cold read, check it against the first-contact checks, tag every finding with its evidence, and give me a scorecard with at most five fixes routed to the right skills. Do not rewrite any copy."
