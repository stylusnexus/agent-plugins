---
name: information-architecture
description: "Use when the user asks to organize product or site content, navigation, menus, labels, taxonomy, categories, facets, URL structure, content types, redirects, or findability. Covers hierarchy and navigation models, naming rules, taxonomy design, findability checks (tree tests, card sorts as plans, scenario walkthroughs), and URL and content-model structure."
---

# Information architecture

Help users understand where they are, what information exists, and how to find or complete what they came for. This is an AI design perspective; it is not user research and cannot show how real people search or group things.

## When to use

- Restructuring navigation, menus, settings or documentation.
- Naming and grouping things; building or cleaning a taxonomy or facets.
- A "people can't find X" report that needs turning into a checkable review.
- Planning a move of pages, URL changes, or a content model.

## Workflow

1. Identify the target users, their tasks, the content or functions in scope and evidence. Mark unknowns MISSING INFORMATION.
2. Inventory the current navigation, labels, content types, relationships and important paths from the product itself or the repository (`findability-checks.md` section 1).
3. Separate observed findability problems from hypotheses. Do not claim research or usability results that were not supplied.
4. Propose a hierarchy, grouping and navigation model (`structure-and-navigation.md`). Prefer familiar language; avoid duplicate paths.
5. Name and classify (`labels-and-taxonomy.md`).
6. Define URLs, content types and relationships, and a redirect plan if anything moves (`url-and-content-model.md`).
7. Check the proposal against important journeys, edge cases, responsive layouts, accessibility and growth (`findability-checks.md`).
8. Return an annotated sitemap or hierarchy, representative task paths, rationale, trade-offs, open questions and acceptance criteria.

## Reference files

| File | Open when |
|---|---|
| `structure-and-navigation.md` | Choosing depth, breadth, navigation model, wayfinding, breadcrumbs, search versus browse |
| `labels-and-taxonomy.md` | Naming things, removing jargon, designing categories and facets |
| `findability-checks.md` | Verifying a proposal; planning tests to run with real people; running scenario walkthroughs |
| `url-and-content-model.md` | Defining URLs, content types, relationships; moving or renaming pages |

## Output format

Sitemap or hierarchy (indented list or table with labels, purpose, owner), label table (current label, proposed label, reason), 5 to 10 task paths ("User wants X: start, steps, destination"), a scenario walkthrough table marked expert review, a list of tests to run with real people, a redirect map where relevant, open questions, acceptance criteria.

## Boundaries

- No invented user research, card-sort results, tree-test scores, search logs or analytics. Plans for tests are plans; mark results MISSING INFORMATION until run.
- AI walkthroughs are expert review, not evidence of user success.
- Product owners keep product, pricing and priority decisions, including what is promoted in navigation.
- Do not publish, merge, deploy, change production redirects or contact users without explicit approval. Redirect maps are proposals.
- No new dependency or design system unless requested and reviewed.
- Keep source-of-truth boundaries intact; navigation does not transfer authority over the data it presents. For dashboards, coordinate with the dashboard designer on signal grouping and decision order.
- Respect the project's licensing and attribution constraints; do not organize or label content in ways that imply licensed material is original or outside its terms.
