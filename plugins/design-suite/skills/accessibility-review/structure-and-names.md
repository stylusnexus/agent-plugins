# Structure and names

Related criteria: 1.1.1, 1.3.1, 2.4.1, 2.4.2, 2.4.4, 2.4.6, 2.5.3, 3.1.1, 3.1.2, 4.1.2.

## First rule of ARIA

Use a native element that already has the semantics and behavior. Add ARIA only when no native element fits. ARIA changes what assistive technology is told; it adds no keyboard behavior, focus, or styling. A role you add is a promise to implement the matching keyboard pattern (WAI-ARIA Authoring Practices).

| Need | Use | Not |
|---|---|---|
| Action on the page | `<button type="button">` | `<div onClick>`, `<a href="#">`, `<span role="button">` |
| Go somewhere | `<a href="/path">` | `<button onClick={router.push}>` |
| Text input, checkbox, radio, select | `<input>`, `<select>`, `<textarea>` | `role="textbox"` on a div |
| Disclosure | `<button aria-expanded>` plus a panel, or `<details><summary>` | click handler on a heading |
| Modal | `<dialog>` with `showModal()` | positioned div with `role="dialog"` only |
| Progress | `<progress>`, `<meter>` | styled divs |

Check: any `onClick` on a non-interactive element (`div`, `span`, `li`, `td`) is at least Serious. It has no role, no focus, no Enter or Space handling (2.1.1, 4.1.2).

## Buttons versus links

- Link: navigates (URL changes, or jumps to a fragment). Button: performs an action or toggles state in place.
- In Next.js use `<Link href>` (renders `<a>`) for navigation. A `<Link>` wrapping a `<button>` is invalid nesting; style the link instead.
- Buttons inside forms need an explicit `type`. Default is `submit`.
- Disabled: prefer `aria-disabled="true"` with a guard in the handler when the control must stay discoverable and focusable; the `disabled` attribute removes it from the tab order. Explain why it is disabled in adjacent text.
- Link text must make sense in context (2.4.4). Flag "click here", "read more" repeated with no distinguishing context. Fix with visible text or `aria-label` that starts with the visible text.

## Landmarks

One of each where the page has it, in this order of preference:
```html
<header>   <!-- banner: only when a direct child of body -->
<nav aria-label="Primary">
<main id="main">   <!-- exactly one -->
<aside aria-label="Related">
<footer>   <!-- contentinfo: when a direct child of body -->
```
- Exactly one `<main>` per page. In the App Router, put it in the layout once; pages must not add a second.
- Two or more `<nav>` (or other repeated landmarks) need distinct accessible names.
- `<section>` and `<form>` become landmarks only with an accessible name; do not name them unless navigation to them is useful.
- All content belongs inside a landmark (best practice; not a WCAG failure by itself).
- Bypass blocks (2.4.1): landmarks or a skip link satisfy this. See `keyboard-and-focus.md` for the skip link.

## Headings

- Exactly one `<h1>` describing the page (best practice; WCAG requires structure to be programmatic, 1.3.1, and headings to be descriptive, 2.4.6).
- Do not skip levels downward (h2 to h4). Choose level by outline, not by font size; restyle with classes.
- Do not use a heading element for visual styling only, and do not fake a heading with a bold `<p>` or `<div class="text-xl font-bold">`.
- Components that render their own heading (cards, dialogs) take a `headingLevel` prop or inherit context, so reuse does not break the outline.
- Check: list the heading outline in the report for each reviewed route.

## Page language and titles

- `<html lang="en">` present and correct (3.1.1). Next.js: set `lang` on `<html>` in `app/layout.tsx`. Inline passages in another language get `lang="fr"` (3.1.2).
- Every route has a unique, descriptive `<title>` (2.4.2). App Router: `export const metadata = { title }` or `generateMetadata`; use a template such as `%s | Product`. Client-side route changes must update the title.

## Accessible names

Name computation order (simplified): `aria-labelledby`, then `aria-label`, then native label (`<label>`, `alt`, `<legend>`, `<caption>`), then content (for buttons, links, tabs, etc.), then `title`/`placeholder` as a last resort. `placeholder` and `title` are not reliable names.

- Visible label wins. If a control has visible text, the name must contain that text, ideally starting with it (2.5.3 Label in Name, A). Voice-control users say what they see.
  - Fail: visible "Search", `aria-label="Find products"`. Pass: `aria-label="Search products"`.
- Icon-only button: `<button aria-label="Close"><svg aria-hidden="true" focusable="false">...</svg></button>`. Or visually hidden text: `<span className="sr-only">Close</span>`.
- Use `aria-labelledby` to reuse visible text, for example a dialog named by its heading: `<dialog aria-labelledby="dlg-title"><h2 id="dlg-title">`. IDs must be unique; in React generate with `useId()`.
- `aria-label` on a `div` or `span` with no role is ignored by many screen readers. Put it on an element with a role.
- Do not repeat the role in the name ("Close button"); the role is already announced.
- Repeated controls ("Edit" x 12) need distinguishing names: `aria-label={`Edit ${item.title}`}`, or `aria-describedby` pointing at the row title.
- Name must not be empty: flag `<button><Icon/></button>`, `<a href><img alt=""></a>` with no other text (4.1.2).

## Common ARIA mistakes

- `aria-hidden="true"` on or around a focusable element: focus lands on something that is silent. Use `inert` or remove from the tab order too. Never `aria-hidden` on `body` or a wrapper that contains the open dialog.
- Redundant roles: `<button role="button">`, `<nav role="navigation">`, `<ul role="list">` (acceptable only to restore list semantics when CSS `list-style: none` removes them in Safari/VoiceOver).
- Conflicting roles: `role="button"` on `<a href>` without space-key handling; `role="heading"` on a button; `role="presentation"` on a focusable element.
- `role="menu"` for ordinary site navigation. Menu roles imply an application-style arrow-key menu; use a disclosure button plus a list of links.
- `aria-label` on content that changes, so name and visible text drift apart.
- Invalid values or missing required pieces: `role="tab"` without `tablist` parent and `aria-selected`; `aria-expanded` on an element that does not control anything; `aria-controls` pointing to a missing id.
- State not updated: `aria-expanded`, `aria-pressed`, `aria-selected`, `aria-current` must change with the UI. Bind them to state, not to initial render.
- `tabindex` greater than 0. Always a finding. `tabindex="0"` only on custom widgets; `tabindex="-1"` for programmatic focus targets.
- `role="alert"` on everything. See `forms-and-errors.md`.

## Images and alt text (1.1.1)

Decide by purpose, not by appearance:
- Informative (conveys content): short alt giving the information, not "image of".
- Functional (inside a link or button): alt describes the action or destination ("Home", not "logo").
- Decorative: `alt=""`. With `next/image`, `alt` is required; pass `alt=""` explicitly for decoration.
- Complex (chart, diagram): short alt naming it plus the data in nearby text or a table.
- Text in images: avoid; if present the alt must carry the same text.
- Inline SVG: decorative gets `aria-hidden="true"`; meaningful gets `role="img"` and `aria-label` or `<title>` linked by `aria-labelledby`.
- CSS background images carry no alt; do not use them for content.

## Symbols, capitals and semantic elements

- Decorative symbols and framing characters (brackets, arrows, slashes, stamp marks, ASCII borders) are hidden from assistive technology (`aria-hidden="true"` on the wrapping span, or applied by CSS), so they are not read aloud.
- Uppercase comes from CSS `text-transform`, not typed capitals, so screen readers and copy-paste see the real text.
- Use the precise element where one exists: `kbd` for keys, `samp` for sample output, `time`, `data`, `dl` for definitions, `output` for calculated results.
- Heading text reads in order and does not depend on `<br>` or split spans for meaning. Inline images inside headings are decorative (`alt=""`) or described.

## Lists and tables (1.3.1)

- Related items use `<ul>/<ol>/<li>`; navigation lists inside `<nav>`.
- Data tables: `<table>`, `<caption>` or `aria-labelledby`, `<th scope="col|row">`. Do not use tables for layout. Do not replace tables with div grids without roles `table`, `row`, `columnheader`, `cell`.
- Sortable column: put a `<button>` in the `<th>` and set `aria-sort` on the `<th>`.
- Do not turn `display: flex` rows into fake tables where the data is tabular.
