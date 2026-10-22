# Structure and navigation

## 1. Hierarchy: depth versus breadth

Recommended starting points (design guidance, not standards; adjust to the content and confirm by testing with people):
- Prefer a broad, shallow structure over a narrow, deep one. Each extra level adds a decision and a chance to pick wrongly.
- Aim for about 2 to 3 levels for most products; justify a fourth level.
- Aim for roughly 5 to 9 items in a primary menu. The "seven plus or minus two" figure describes memory, not menus, so treat it as a rough comfort range, not a rule. Longer lists are acceptable when they are scannable, well grouped and familiar (alphabetical lists of countries).
- Every level should have a clear grouping principle, stated in one sentence. If you cannot state it, the grouping is probably arbitrary.
- Categories should be mutually distinct to the user. Items that could reasonably live in two places signal a labelling or grouping problem.
- A category with a single child should usually be collapsed. A catch-all "Other" or "Misc" is a warning sign; resolve it.
- Avoid placing the same thing in several places. If cross-links are needed, make one location canonical and link from the others.
- Long lists get structure: group into 2 or 3 chunks, tab or disclose the rest, or show the top few with a link to the full list.
- On content and marketing pages each section carries one message: a short heading, one supporting line, one visual or action.
- The primary navigation fits on one line at desktop width; if it does not, cut or condense items rather than wrap. Keep its height modest (about 64-80px, recommended).

## 2. Organising principles

Choose one primary principle per level and use it consistently:
- By task or goal (what users are trying to do) - usually best for application navigation.
- By audience (for X) - only if audiences truly have different content and know which they are.
- By topic or subject - for content libraries and documentation.
- By object or entity (projects, people, reports) - for data-centred apps.
- By lifecycle stage or time - for processes.
- By alphabet or number - for lookup lists where the user knows the name.
Avoid organising by your internal structure (team, system, department) unless users think that way.

## 3. Navigation models

| Model | Use | Notes |
|---|---|---|
| Global (primary) | Top-level sections visible everywhere | Same position and order on every page; current section indicated |
| Local / sub-navigation | Siblings within a section | Show siblings and current item |
| Contextual | Links within content to related items | Use for "next" and "related" not as the only route |
| Utility | Account, settings, help, notifications | Keep separate from content navigation |
| Hub and spoke | Dashboard or home to isolated tasks | Return path to the hub must be obvious |
| Sequential / wizard | Ordered steps | Show step count and allow safe back |
| Faceted | Large catalogs with attributes | See labels-and-taxonomy.md |
| Search | Large or unpredictable content | Complement, not replacement, for browse |

For mobile patterns (bottom bar, drawer) see the mobile-design skill.

## 4. Wayfinding

Users should always be able to answer: where am I, where can I go, how did I get here, how do I go back.
- Page title (H1) matches the nav label that led to it.
- Current location highlighted in navigation (not by colour alone) and exposed to assistive technology (`aria-current`).
- Consistent headings and page structure within a type.
- Visited and unvisited states for links when helpful.
- Clear labels on links (describe destination) and no "click here".
- Landmarks (`nav`, `main`, `header`) with labels where there are several navs.
- Skip link to main content.
- Provide the same navigation items across responsive layouts; changing the pattern is fine, removing items is a finding.

## 5. Breadcrumbs

- Use for hierarchies of three or more levels or when pages are reached by many routes.
- Show the location path (hierarchy), not the user's history, and not a replacement for primary nav.
- Last item is the current page, not a link (or marked with `aria-current="page"`).
- Wrap in `nav` with an accessible name ("Breadcrumb"); present as an ordered list.
- On narrow screens, collapse middle levels but keep the parent and a way to the root.
- Do not add breadcrumbs to flat sites; they add noise.

## 6. Search versus browse

- Browse supports discovery and learning the structure; search supports known-item lookup.
- Offer search when content volume or variety makes browsing slow. Recommended trigger (a heuristic): offer a visible search box once users must choose among many items or levels; confirm by testing.
- A search box should look like one, sit in a consistent place, and be big enough for typical queries.
- Search results: show why each result matched, its type and location, and handle no results (suggest alternatives, spelling, broader terms, clear filters).
- Provide scoped search ("in this project") only if scope is shown and changeable.
- Do not rely on search to rescue a broken structure; it hides the problem.
- Synonyms: capture alternative terms users plausibly use as search aliases (from supplied search logs, support questions or interviews; mark MISSING INFORMATION when none exist).

## 7. Growth and maintenance

- Plan where new items go before they arrive: write the rule for adding to a category and for splitting one.
- Set an owner for each section and a review trigger (for example when a category exceeds the size the team finds scannable; threshold chosen with the product owners).
- Avoid structures that need a redesign for every new item.
- Keep a changelog of structural changes so redirects and docs can follow (see url-and-content-model.md).

## Marketing pages only

- Eyebrow labels sparingly: at most one for every three sections (recommended). If the heading does the job, drop it.
- A hero holds one headline, one short line and its actions. Tagline strips, pricing teasers and stat rows move down the page.
- Trust and logo sections sit below the first view, not inside the hero. Only real logos, used with permission.

## 8. Output template

```
Hierarchy
1. Section (purpose, grouping principle)
   1.1 Child (type, owner)
Task paths
T1: <user goal> | start: <page> | steps: A > B > C | destination: <page> | notes
Duplicated or ambiguous placements: <list>
Removed or merged: <list with reason>
```
