# Labels and taxonomy

## 1. Labelling rules

1. Use the words your users use, taken from their messages, support questions, search terms or interviews if supplied. Without that evidence, choose plain everyday words and mark the label as an unverified proposal.
2. Be specific and concise. "Billing" beats "Account services"; "Team members" beats "Users and groups management".
3. Lead with the distinguishing word ("Invoices", "Invoice settings", not "Settings for invoices").
4. Describe the destination or the action, not the feature's marketing name.
5. Verbs for actions ("Export report"), nouns for places ("Reports").
6. Same thing, same word, everywhere (not "Contact", "Get in touch" and "Talk to us" for one action in one flow). Same word never for two different things.
7. Keep labels parallel within a list (all nouns, or all verbs; same grammatical form).
8. Sentence case, no ALL CAPS, no unexplained abbreviations or acronyms.
9. Avoid vague catch-alls: "Misc", "Other", "Resources", "More", "Tools", "General".
10. Avoid "click here" and "learn more" as links without context; link text should make sense out of context (screen-reader link lists).
11. Make sure the label matches the page title it leads to.
12. Do not hide meaning in icons alone; pair with text, particularly for navigation.
13. Keep labels short enough to fit narrow layouts without truncation.
14. A section label names the topic in plain words. No counters ("Section 03", "Stage 2"), no jargon, no category label under a logo. Numbers are fine for a real sequential process.

## 2. Naming consistency audit

1. List every label across navigation, page titles, buttons, breadcrumbs, emails and docs for one concept.
2. Group variants ("Project", "Workspace", "Space" for the same thing).
3. Choose one term; record the decision and who owns it.
4. Search the codebase and content for other occurrences; list files.
5. Check that the term in the interface matches the term in the URL and in help (see url-and-content-model.md).

| Concept | Variants found | Chosen term | Where to change | Notes |

## 3. Avoiding internal jargon

Internal jargon includes team names, system names, ticket or project codenames, database table names, and acronyms.
- Test: would a new user know it? If it came from inside the company and is not in the user's vocabulary, replace or define it.
- Product names are fine when the user already knows them. Otherwise add a descriptor.
- If a technical term is the right term for the audience (developers), keep it, but define on first use.
- Do not translate a precise term to a vague one just to sound friendly.
- Mark each substitution as a proposal to be confirmed by someone who knows the audience.

## 4. Taxonomy design

A taxonomy classifies content or entities so they can be grouped, filtered and reported.

1. Define scope and purpose: what decisions or findability tasks does it serve? A taxonomy without a use should not exist.
2. Choose structure:
   - Flat list of tags: simple, grows messy.
   - Hierarchy (parent/child): needs a single clear parent per item (or polyhierarchy by design).
   - Facets: independent attributes combinable by filters.
3. Write a definition (scope note) for every term, and what it excludes.
4. Rules for terms:
   - Mutually exclusive within a level where an item must have one value.
   - Collectively exhaustive for the chosen scope, with an explicit "Not set" and a rule for unknown, not "Other".
   - Singular or plural consistently.
   - Stable identifiers separate from display labels, so renaming a label does not break data or URLs.
5. Governance: who may add a term, how duplicates and synonyms are handled, when to retire a term (keep a redirect or alias), how to review. Product owners decide product-level categories.
6. Size: keep each list scannable; split large lists by a second attribute rather than adding more items. No fixed number is a standard.
7. Avoid classification by time-sensitive status ("New", "Latest") that goes stale.
8. Keep user-facing taxonomies separate from internal ones when they diverge; map between them.

## 5. Facets

- A facet is one attribute with a set of values (type, status, owner, date, tag).
- Choose facets users actually use to narrow (supplied evidence or unverified proposal).
- Facets should be independent of each other and each item should have a value for every facet (or "Not set").
- Order facets by usefulness; order values by frequency or logic (date, size), not alphabet by default.
- Show counts only if accurate and fast; show the active filters, an obvious "Clear all", and what zero results means ("0 results for Status: Closed and Owner: me").
- Disable or hide combinations that yield nothing only if the reason is communicated.
- Allow multi-select within a facet (OR) and combine across facets (AND), and say so.
- Keep filter state in the URL where people may share or return (see url-and-content-model.md).
- Facets work with keyboard and screen reader (grouped controls with labels, live result-count update).
- Mobile: put facets in a sheet or page with an "Apply" and visible count of results.

## 6. Checks

- Every label is in the label table with current, proposed, reason, evidence or MISSING INFORMATION.
- No concept has two names; no name has two concepts.
- No "Other" bucket without an owner and a plan to dissolve it.
- Each taxonomy term has a definition and an owner.
- Renaming a term does not break identifiers, URLs or saved filters.
