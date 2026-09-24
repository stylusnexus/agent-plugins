# Touchpoint audit

A launch post is one door. This audit covers the rest of them — the same plain-language, accessibility, and truthful-claims bars from [the pre-publish content check](../../mk-copy/references/pre-publish-content-checklist.md), applied to every place a stranger actually meets the product on day one, not just the announcement itself.

## Why this can't be skipped
The sources behind these checks exist because a real share of any audience hits exactly these gaps: a screen-reader user needing real alt text and descriptive link text (Source: W3C, "Introduction to Web Accessibility," https://www.w3.org/WAI/fundamentals/accessibility-intro/, accessed 2026-09-24), a first-time reader needing a page written for a first read, not a second one (Source: digital.gov, "Plain language," https://digital.gov/guides/plain-language, accessed 2026-09-24). A launch that gets the headline right and skips these fails a real fraction of the people it reaches, not a hypothetical edge case.

Checking value across every customer-facing touchpoint, not just the ad or announcement, is the core idea of Yoram (Jerry) Wind and Catharine Findiesen Hays's book *Beyond Advertising: Creating Value Through All Customer Touchpoints* (Wiley, 2016); credited here for the idea, not followed for its specific model. Source: Wharton Executive Education, "Beyond Advertising" — https://executiveeducation.wharton.upenn.edu/thought-leadership/wharton-at-work/2016/05/beyond-advertising/

## The touchpoints, and what to check on each
- **Landing page** — plain-language and accessibility checks from the pre-publish content check; the headline alone should tell a stranger what the product does.
- **README** (if the product is open-source) — same checks; treated as the actual landing page for that audience.
- **Onboarding / first-run flow** — every screen readable on a first pass, every required field explained, no step assuming context the reader doesn't have yet.
- **Empty states** — what a brand-new user sees before they've done anything; an empty state with no guidance reads as broken, not as new.
- **Error messages** — say what happened and what to do next, in plain language; no raw stack traces or bare codes shown to a non-technical user with no explanation.
- **Signup / confirmation email** — the first message a new user gets; checked against the same plain-language bar, with no unsourced claim in it.
- **Pricing page** — every number accurate as of launch day, and any comparison to a competitor's price checked against that competitor's current, real published price, not a remembered one.
- **Support inbox / contact path** — a real, working way to reach a human, visible without hunting; a missing or buried contact path is a trust gap under the same guidance the pre-publish check uses, not a minor omission.
- **Changelog / release notes** — accurate as of the actual shipped version, not the originally planned one.

## Running the audit
For each touchpoint: note whether it exists, whether it's been checked against the sources above, and whether any gap found needs a fix before launch or can ship as a known gap with an owner and a date. Mark each row "ready" or "not ready." An audit that comes back with every row marked "ready" the first time through usually means it wasn't looked at hard enough, not that everything is actually fine.

| Touchpoint | Exists? | Checked against plain-language / accessibility / truthful-claims bar | Ready / Not ready | Owner | Fix by |
|---|---|---|---|---|---|
| Landing page | | | | | |
| README | | | | | |
| Onboarding | | | | | |
| Empty states | | | | | |
| Error messages | | | | | |
| Signup/confirmation email | | | | | |
| Pricing page | | | | | |
| Support inbox | | | | | |
| Changelog | | | | | |
