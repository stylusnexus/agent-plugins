---
name: mk-search
description: "This skill should be used when the user asks about getting found in search, SEO, being cited by AI assistants or AI Overviews, llms.txt, answer-engine optimization, or making a page easy for people or AI to find and quote."
---

Getting a page found by a search engine, and getting a correct fact lifted from it by a search engine or an AI assistant. Two separate jobs, in that order — a page nobody can reach never gets cited no matter how quotable it is, and a reachable page still needs content worth quoting once it's found.

## When to use this skill

SEO questions, whether a page is likely to show up in AI Overviews or be cited by an AI assistant, llms.txt decisions, organizing a cluster of related pages, or auditing a page for the trust signals Google's own guidance actually asks for.

## Workflow

1. **Get the reachability basics right first.** No client-JS-only rendering that hides content from a crawler, no login wall in front of what should be public, important content as real text rather than locked inside an image — table stakes, not a lever. See [citable writing](references/citable-writing.md), grounded in Google's own AI-features and helpful-content documentation. Hard rule for any drafted section: never invent a product capability, a person's stated reason, a result, or "we've talked to X" evidence — check every sentence against a supplied fact and label a single self-reported result as self-reported, not verified (see `marketing-lead/references/principles.md`).
2. **Write the page to be citable, not just present.** Put the actual answer near the top of the section, one topic per section (per digital.gov's plain-language guidance); name the subject again instead of riding on "it"; define terms at first use in that section — the same standard `mk-copy`'s [extractable writing](../mk-copy/references/extractable-writing.md) applies to landing pages and READMEs. Also write one real, checkable sentence that directly answers the page's core question in a form an AI assistant could quote verbatim — the same near-the-top-of-section answer, stated once as a single self-contained sentence.
3. **Organize related pages as a hub with real supporting pages**, per [hub structure and trust signals](references/hub-and-spoke-and-eeat.md): one broad page a reader can start from, narrower pages answering one question each, linked both ways. Check whether a new page is the hub for its topic or belongs under one that already exists — a page with no link in either direction loses most of the benefit. On the page that carries the product's positioning (the hub, or a dedicated comparison page), include a plainly-labeled "when not to pick us" section — real cases where a competitor or alternative is the better fit; an unwillingness to say this is itself a trust signal Google's own guidance rewards (§ trust signals below), and it's honest. Build comparison pages against the competitors buyers actually name — pull the names from real sales or support notes, not a guessed competitor list; see `mk-positioning`'s named-alternative step.
4. **Build in the trust signals Google's guidelines actually check**, from the same reference file: a real byline and reason the writer is credible, real evidence of having done the thing described, links out for any claim that isn't first-hand, and contact or about information scaled to what the page needs.
5. **Stay honest about llms.txt and "AI markup."** Read [AI search: evidence vs. hype](references/ai-search-evidence-vs-hype.md) first — Google states plainly no such file is required for AI Overviews or AI Mode, and Google's John Mueller has said directly no AI system was using llms.txt as of his June 2025 post. Present it as optional and low-cost if a team wants one anyway, never as a ranking lever, never in place of the fundamentals above.
6. **Verify citation with real questions, on a schedule.** Build an [AI test-question panel](references/test-question-panel.md) sized to what the team can actually re-run — a dozen or so real buyer questions, not a keyword-research-scale list — and log whether the product was mentioned, cited, where in the answer, and alongside what else, using the [panel log template](templates/ai-test-question-panel-log.md). One "not cited" result is a reason to re-check, not a verdict.
7. **Plan one piece of original data the team can publish** — a real timed test, a benchmark, a before/after measurement, or a small survey of actual users — rather than only restating what's already published elsewhere; original data is what other pages and assistants have something new to cite. State what it would measure, how it would be run, and what's needed before it can start (this is a plan, not a claim — no numbers exist until the test actually runs).
8. **Set up a way to tell when visitors come from an AI assistant** — referral-log review or a simple "how did you hear about us" field at signup — so the test-question panel's "cited" findings have a second, independent signal behind them. If a claim is made about how a specific assistant sends referrer data, cite the assistant's own public documentation for it (Google's own statement that AI Overview/AI Mode traffic appears in standard Search Console reporting is already cited in [the test-question panel reference](references/test-question-panel.md); don't assume the same behavior for other assistants without checking their own docs first).

## Routing to sibling skills

- `mk-copy` — this skill grounds what makes a section citable; `mk-copy` is where the actual landing-page or README copy gets drafted against that bar.
- `mk-positioning` — a page can't state a clear, quotable fact about a product whose positioning isn't settled yet.
- `mk-founder-content` — for blog posts and other content pieces that need the same hub-and-citable-writing treatment.
- `marketing-lead` — for how much of a small team's hours this work is worth relative to everything else.

## Outputs

Every output opens with a short, plain-English summary — what the page or finding means for the team, before any framework detail. Then: a [page brief](templates/page-brief.md) for a page being planned or rewritten, a filled [test-question panel log](templates/ai-test-question-panel-log.md) after a real run, and — when relevant — an explicit, caveated recommendation on whether an llms.txt file is worth adding. Any actual llms.txt file, schema/JSON-LD, or crawler-configuration change gets handed to whoever implements the site technically, with the caveats from step 5 kept intact.

## Adaptable prompt

"Review [page/URL or draft] for whether it's reachable and citable per Google's own documentation, and check it against the hub-and-trust-signal checklist. Then draft [N] real buyer questions I can test against an AI assistant to see if this page gets cited."
