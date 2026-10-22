# Keyboard and focus

Related criteria: 2.1.1, 2.1.2, 2.1.4, 2.4.1, 2.4.3, 2.4.7, 2.4.11 (new in 2.2), 2.4.13 (new in 2.2, AAA), 3.2.1, 3.2.2, 1.4.13.

## Operability (2.1.1, A)

Every function available by pointer must work from the keyboard alone, without timing-dependent keystrokes. Source-pass checks:
- Handlers on non-interactive elements (`div onClick`) with no role, `tabindex`, and key handling: Blocker if it is a core action.
- `onMouseDown`/`onMouseEnter`-only behavior (hover menus, tooltips that hold needed content, hover-reveal buttons) with no focus equivalent. Add `onFocus`/`:focus-within`.
- Drag-only interactions need a keyboard path (see 2.5.7 in `target-size-and-motion.md`).
- Hover-only reveals (hover-expanding accordions, hover menus) need a keyboard and touch equivalent; click or focus must do the same job.
- Pinned or hijacked scroll must not trap keyboard users, and focus order matches visual order. `grid-auto-flow: dense` can separate the two; flag it.
- A menu control that opens a full-screen overlay manages focus: moves in, closes on Esc, returns focus to the control.
- Native `button` activates on Enter and Space; native `a[href]` on Enter only. Custom `role="button"` must handle both.
- Custom scroll containers that hold content need `tabindex="0"` (and a name) so keyboard users can scroll them, unless they contain focusable children.

## No trap (2.1.2, A)

Focus can always be moved away using standard keys (Tab, Shift+Tab, Esc, arrows). If a non-standard key is needed, the user must be told. Modal dialogs legitimately contain Tab only while open and must close with Esc and a visible control. Check embedded iframes, rich-text editors (Tab inserting indentation), maps, and code editors: each needs a documented escape.

## Focus order (2.4.3, A) and DOM order

- Tab order follows DOM order. CSS `order`, `flex-direction: row-reverse`, grid placement, and absolute positioning can make visual order differ from DOM order; flag when the mismatch changes meaning.
- Never use `tabindex` > 0.
- Dynamic content inserted earlier in the DOM than the user's position shifts focus context. Insert after, or move focus deliberately.
- When an element that holds focus is removed (deleted row, closed popover), move focus to a sensible neighbor or container heading. Otherwise focus resets to `body` and the user loses their place.
- After client-side navigation, Next.js includes a route announcer that reads `document.title`, then the `h1`, then the URL path (Next.js accessibility docs). Those docs describe no focus move, so confirm focus placement in a browser. A common fix is focusing the `h1` with `tabIndex={-1}` on route change.
- Changing context on focus or on input without warning is a failure of 3.2.1 / 3.2.2 (for example a `select` that navigates on `onChange`).

## Visible focus (2.4.7, AA)

Keyboard focus indicator must be visible on every focusable element in every theme.
```css
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
```
- `:focus-visible` shows the ring for keyboard focus and hides it for mouse clicks on buttons; text inputs always match it. Prefer it over bare `:focus`.
- Flag `outline: none`, `outline-0`, `focus:outline-none`, or `ring-0` without a replacement indicator. In Tailwind v3 `outline-none` keeps a transparent outline (visible in forced-colors mode). In v4 `outline-none` sets `outline-style: none` and the old behaviour was renamed `outline-hidden` (Tailwind v4 upgrade guide). Check which version the project uses.
- Tailwind pattern: `focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600`.
- Do not rely on a color change of background alone, a thin box-shadow with low contrast, or `border-color` change of 1px.
- Indicator contrast against adjacent colors is 3:1 minimum (1.4.11; see `contrast-and-colour.md`). Check against both the component and the page background, in light and dark.
- `outline` follows `border-radius` in modern browsers; `overflow: hidden` on a parent clips outlines and box-shadow rings. Use `outline-offset` negative or pad the container.
- Forced colors: `box-shadow` rings disappear in Windows high-contrast; outlines survive. Prefer outline.

### Focus Not Obscured, Minimum (2.4.11, AA, new in 2.2)

When a component receives keyboard focus, it must not be entirely hidden by author-created content (sticky header, cookie banner, chat widget, bottom bar). Partly hidden passes at AA; the enhanced criterion (2.4.12, AAA) requires none hidden.
```css
html { scroll-padding-top: 5rem; scroll-padding-bottom: 4rem; } /* >= sticky bar heights */
```
Test by tabbing through a page at 200 percent zoom and 320 px width with all sticky elements showing. Also check items inside modals under a sticky footer.

### Focus Appearance (2.4.13, AAA, new in 2.2)

Not required at AA. As design guidance: a focus indicator that is at least as large as a 2 CSS px thick perimeter of the component, with at least 3:1 contrast between focused and unfocused states, satisfies the intent. Report gaps as Minor unless the user targets AAA.

## Skip link (2.4.1, A)

Required unless landmarks provide an adequate bypass; a skip link is still the most reliable. First focusable element in the document:
```tsx
<a href="#main" className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-4 focus:z-50 focus:rounded focus:bg-white focus:px-3 focus:py-2">Skip to main content</a>
...
<main id="main" tabIndex={-1}>
```
Check: link becomes visible on focus, target exists, target receives focus (some browsers move sequential focus start only; `tabIndex={-1}` on main makes it reliable), and sticky headers do not cover it.

## Modal dialogs

Prefer native `<dialog>`:
```tsx
const ref = useRef<HTMLDialogElement>(null);
// open: ref.current?.showModal();  close: ref.current?.close();
<dialog ref={ref} aria-labelledby={titleId} onClose={() => triggerRef.current?.focus()}>
  <h2 id={titleId}>Delete project</h2>
  <button type="button" autoFocus>Cancel</button>
</dialog>
```
`showModal()` makes the rest of the page inert, moves focus into the dialog, closes on Esc, and renders a backdrop. The HTML spec's close steps return focus to the previously focused element when focus was inside the dialog or the dialog was modal, with no check that the element still exists. Browser behaviour was not tested here, so verify it; if the trigger was removed, restore focus manually. Use `show()`/non-modal only for non-modal popovers.

If a custom dialog (or a library like Radix/Headless UI, which handle this) is used, require all of:
1. `role="dialog"` (or `alertdialog` for confirmations that need a response) with an accessible name; `aria-modal="true"`.
2. Focus moves in on open: first focusable element, or the dialog container with `tabindex="-1"`, or the least destructive control for destructive confirms.
3. Tab and Shift+Tab cycle inside; background is `inert` (preferred) or `aria-hidden`.
4. Esc closes, and a visible close control exists.
5. On close, focus returns to the control that opened it.
6. Page scroll behind is locked without layout shift.
Do not put focus on a close button hidden off-screen.

## Roving tabindex and composite widgets

Tabs, toolbars, radio groups, listboxes, menus, trees, grids are one tab stop; arrows move within (WAI-ARIA Authoring Practices keyboard tables).
- Roving tabindex: active item `tabindex="0"`, others `-1`; arrow keys move and update. Alternative: `aria-activedescendant` on the container.
- Tabs: `role=tablist/tab/tabpanel`; Left/Right move (Up/Down if vertical); Home/End to first/last; `aria-selected`, `aria-controls`, panel `aria-labelledby`. Choose automatic or manual activation and keep it consistent.
- Radio group: native `<input type="radio">` with same `name` does this for free. Prefer it.
- Menu button: Enter/Space/Down opens, arrows move, Esc closes and returns focus to the button, Tab closes. Use `role="menu"` only for action menus, not navigation.
- Combobox/autocomplete is the hardest pattern; prefer a native `select` or a vetted library. Check `aria-expanded`, `aria-controls`, `aria-activedescendant`, and announcement of result counts.
- Home/End and Type-ahead are expected in listboxes and menus; flag if absent but rate Moderate.

## Custom controls

A custom control must provide: role, name, state/value (4.1.2), focusability, keyboard activation, visible focus, and state exposure through ARIA attributes bound to React state. Custom checkbox: keep the real `<input type="checkbox">` visually hidden but focusable (`sr-only` plus `peer`), and style the sibling with `peer-focus-visible:`. Do not use `display: none` or `visibility: hidden` on the input; that removes it from the tab order.

## Keyboard shortcuts (2.1.4, A)

Single-character shortcuts (letters, digits, punctuation) must be turn-off-able, remappable, or active only when the relevant component has focus. Modifier combinations avoid the issue but must not collide with browser and screen-reader keys. Document shortcuts and make them discoverable.

## Hover and focus content (1.4.13, AA)

Tooltips and popovers shown on hover or focus must be dismissible without moving pointer or focus (Esc), hoverable (pointer can move onto the content without it vanishing), and persistent until dismissed or no longer relevant. Use `aria-describedby` to tie tooltip text to its trigger. Tooltips must not be the only place essential information lives.
