# Component patterns

Related criteria: 1.4.1, 1.4.13, 2.1.1, 2.4.3, 3.2.2, 4.1.2, 4.1.3. Use this file when the surface contains a named widget. It adds the pass/fail check per component; general rules stay in `keyboard-and-focus.md`, `forms-and-errors.md` and `structure-and-names.md`. Most items are NEEDS-TEST in a browser or VoiceOver unless the source shows the failure outright.

## Toggle button and switch

- Pass: `<button type="button" aria-pressed="true|false">`. Fail: a link, or a `div` with a click handler.
- The label stays constant ("Mute", not "Mute" then "Unmute") while `aria-pressed` changes. Changing both makes the state read backwards. Check: press it and read the accessible name before and after; it must be identical.
- Switch: `role="switch"` with `aria-checked`, named by the visible text (`aria-labelledby`). A native checkbox with a clear label is the simpler replacement.

## Tabs

- Ask first: do users need tabs at all? Short or sequential sections work as headings plus a table of contents (Minor if unneeded).
- Pass: one tab stop for the tablist, arrow keys move between tabs (wrapping is fine), Tab leaves to the panel.
- Non-selected tabs carry `tabindex="-1"`; selected tab and panel are linked by `aria-controls` and `aria-labelledby`.
- On narrow screens, fall back to a table of contents of in-page links, not to an accordion. Check at 320 CSS px that the same content is reachable without a tab pattern.

## Collapsible section

- Pass: a button inside the heading (`<h3><button aria-expanded>Title</button></h3>`) so heading navigation still works. Fail: heading with a click handler, or a button wrapping the heading.
- State lives on the control (`aria-expanded`), and the panel uses `hidden`. Do not depend on `aria-controls` being announced.

## Navigation menu versus ARIA menu

- Nested lists of links are navigation: `<nav>` with a list, not `role="menu"`. `role="menu"` promises arrow-key app behaviour the links do not have. Report as Serious.
- A collapsed site menu is a button with `aria-expanded` that reveals the list. Closed items are hidden from tab order and screen reader (`hidden`), and the list stays inside the `nav`.
- Check: closed menu items are not reachable by Tab; after opening, the first link is next in focus order.

## True menu button (actions only)

- Pass: `aria-haspopup`, `aria-expanded`, `role="menu"` and `menuitem`, roving `tabindex`, arrow keys move, Esc closes and returns focus to the button, choosing an item returns focus too.
- A persisted choice uses `menuitemradio` with `aria-checked`; focus the checked item on open.

## Tooltip versus toggletip

- A tooltip either names the control (linked with `aria-labelledby`) or describes it (`aria-describedby`). One that is only visual and missing from the accessible name fails 4.1.2. It shows on focus and hover and, per 1.4.13, is dismissible (Esc), hoverable and persistent. No interactive content inside.
- A toggletip is for on-demand help: a `button` that, on click, fills a live region (`role="status"`) after a short delay (about 100 ms, recommended). Fail: toggletip on a non-button, or text added to `aria-describedby` only.

## Carousel (content slider)

- Baseline pattern: items in a list inside a horizontally scrolling container. It moves only when the user moves it; no auto-rotation.
- The scroll container gets `tabindex="0"`, a role and name (for example `role="region"` with a label) so arrow keys scroll it.
- Prev/next buttons are optional extras. Off-screen links are removed from tab order, but the content is not `aria-hidden`.

## Select used as navigation

- Fail (3.2.2): `onChange` that navigates or submits. Replace with a list of links, or a select plus an explicit Go button.

## Disabled buttons

- Native `disabled` drops the control from tab order and loses focus if it was focused. Prefer `aria-disabled="true"`, keep it focusable, ignore the activation, and explain why in text next to it.

## Deletion and removal

- After deleting an item, focus the next or previous item. If the list is now empty, focus the list heading (`tabindex="-1"`).
- Announce "Item deleted." through a polite status region, not by moving focus alone.

## Status messages

- Information-only updates go to `role="status"` (polite) that already exists in the DOM. Do not move focus for them. Use `role="alert"` only for failures that block the task.
- Prefix message type in text ("Error:", "Info:"), not by colour or icon alone.
- Check: type in a field while the message fires; focus must stay put.

## Theme switch

- Respect `prefers-color-scheme` on first load, then store the user's choice.
- Put the switch in a landmark (header or footer), in the same place on every page.
- Forced-colours safe: no content in background images, `currentColor` on SVG, transparent border on buttons. Check in Windows high contrast or forced-colors emulation.

## Load more

- A real button replaces infinite scroll. On activation, move focus to the first new item and announce the count politely.

## Icon-only controls

- Name through visually hidden text or `aria-label`; set `focusable="false"` on the SVG; use `currentColor` so forced colours work.

## Report by component

Group findings by component and name one replacement, not one ticket per WCAG criterion. A single custom button can fail 1.1.1, 2.1.1 and 4.1.2; the fix is `<button>`, not three patches.

Mini example:
- ID A-07, component: "Filter" toggle (`FilterChip.tsx:41`). Observed: `div onClick`, label changes "Show"/"Hide". Criteria: 2.1.1, 4.1.2. Priority: Serious. Fix: native `<button type="button" aria-pressed>` with a fixed label. Evidence: VERIFIED (source); VoiceOver output NEEDS-TEST.
