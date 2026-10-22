# URLs and content model

## 1. URL structure

URLs are part of the interface: people read, share, bookmark and return to them.
- Readable and predictable: lowercase, hyphens between words, words from the user's vocabulary (match the label; see labels-and-taxonomy.md).
- Reflect the hierarchy where it is stable: `/projects/northwind/invoices`.
- Stable identifiers in the path or query so titles can change without breaking links: `/projects/1234-northwind` (id first or alongside; slug is decorative).
- One canonical URL per page. Where duplicates exist (trailing slash, query order, uppercase), redirect to the canonical and declare `rel="canonical"`.
- Do not include implementation details (file extensions, framework names, session ids).
- Keep URLs short; avoid deep nesting beyond what the hierarchy needs.
- Filters, sort and pagination in query parameters so state can be shared and survives reload: `?status=open&sort=updated`. Keep parameter names stable and documented.
- Do not put secrets, personal data or tokens in URLs (they leak in logs, referrers, history).
- Every meaningful view in an app has its own URL; modals that represent a place may too (see mobile-design for back behaviour).
- Avoid changing URLs for cosmetic reasons.
- Reserve paths for future sections where known; avoid collisions with user-generated slugs.
- Internationalisation: decide path prefix versus domain per language, keep a consistent pattern.

## 2. Content types

A content type is a repeatable kind of content with defined fields. For each, document:

| Field | Meaning |
|---|---|
| Name | Plain label ("Guide", "Release note") |
| Purpose | The task or question it serves |
| Fields | Required and optional, with type, limits, and who supplies each |
| Template | Which page layout renders it |
| Owner | Who keeps it current |
| Lifecycle | Draft, review, published, archived; who may change state |
| URL pattern | e.g. `/guides/{slug}` |
| Source of truth | Where the authoritative copy lives |

Rules:
- Create a new type only when structure, layout, or lifecycle truly differ; otherwise add a field or a tag.
- Fields hold one kind of thing; avoid a free-text field that mixes several.
- Separate content from presentation so one item can appear in several places (list, search result, related links).
- Mark which fields drive navigation, filtering and search. Those need controlled values (see taxonomy rules).
- Required summary or description fields help search and listing.
- Content fields for licensed material must record licence and attribution status so it stays inside its terms.

## 3. Relationships

Document how types relate:
- One-to-many: project has many tasks.
- Many-to-many: article has many tags; tag has many articles.
- Hierarchy: parent and child.
- Ordered sequences: steps in a guide.
- References: "related to", "replaces", "supersedes".

For each relationship: direction, cardinality, whether deleting the parent affects children, and how it appears in the interface (breadcrumb, related list, filter). Draw a simple entity relationship diagram or table. Relationship display should be derived from data rather than hand-maintained links.

| From | Relationship | To | Cardinality | Shown as | On delete |

Check that every item has at least one route in (from navigation, search or a parent) and, where useful, a route out (next, related).

## 4. Moving, renaming and retiring pages

Before changing any URL:
1. Inventory old URLs (from the sitemap, routes, analytics if supplied, backlinks if available, internal links, docs, emails, bookmarks).
2. Define each old-to-new mapping in a redirect map.
3. Prefer the most specific match; avoid sending everything to the home page.
4. Use a permanent redirect (HTTP 301 or 308) for moved content, a temporary redirect (302 or 307) only for temporary moves, and 410 or a helpful 404 page for deliberately removed content with a link to the nearest alternative.
5. Avoid redirect chains and loops; redirect old directly to the final URL. Test.
6. Update internal links, sitemap, canonical tags, navigation, breadcrumbs and in-product references, so they no longer rely on the redirect.
7. Preserve query parameters and anchors where meaningful.
8. Keep redirects in place for a long time; removing them breaks old links. A retention period is an owner decision.
9. Keep a 404 page that helps: search, navigation, and a link home.
10. For apps: handle renamed routes for saved bookmarks and deep links in emails or notifications already sent.

Redirect map format:

| Old URL | New URL | Type (301/302/410) | Reason | Verified? |

Applying redirects changes the live site. Produce the map as a proposal; deploying it needs explicit product owner approval.

## 4a. Restyling without restructuring

A visual change must not move these without explicit product owner approval: URLs, slugs and anchors; primary navigation labels; form field names and order (they feed autofill and tracking); the logo; legal and consent text; analytics event names. Before touching a layout, record the current page tree, main navigation and key conversion paths so the result can be compared.

## 5. Checks

- Every page has one canonical URL.
- All old URLs in the map resolve in one hop to a working page.
- No internal link points at a redirected URL.
- Content types have owners and lifecycle.
- Relationship table covers every reference in the interface.
- URLs match labels and do not expose private data.
