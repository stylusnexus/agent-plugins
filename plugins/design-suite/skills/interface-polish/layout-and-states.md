# Layout and states

## Grouping and proximity

- Related items sit closer together than unrelated items. Measure: the gap inside a group is clearly smaller than the gap between groups (for example 8px inside, 24-32px between).
- Group with whitespace first, then alignment, then a container or divider as a last resort.
- A label sits closer to the control it labels than to the previous control.
- Actions sit with the content they act on. Destructive actions are separated from routine ones.

## Alignment

- Pick one alignment edge per column of content and hold it. Left-align text in left-to-right languages; avoid centred paragraphs of more than two or three lines.
- Align baselines when text of different sizes shares a row (`items-baseline`), and centres when icons or controls share a row (`items-center`).
- Numbers align right (with tabular numerals); text aligns left; headers align with their column.
- Use CSS grid for two-dimensional alignment instead of matching widths by hand.
- Use logical properties (`ms-`, `me-`, `ps-`, `pe-`, `text-start`) where the product may support right-to-left languages.

## Reading order

- The visual order matches the DOM order. If CSS reorders items (`order-*`, `flex-row-reverse`, grid placement), keyboard and screen-reader order will differ; avoid it or confirm with accessibility-review.
- The primary action and the main heading are the most prominent items on the screen. One primary button per view or section.
- Place the next step where the eye ends: for forms, below the last field; for dialogs, bottom edge.

## Responsive structure

- Build fluid first: use `%`, `fr`, `minmax()`, `flex-wrap`, and `clamp()` so the layout adapts without breakpoints.
- Add a breakpoint only where the content breaks (a line gets too long, a column gets too narrow, a table overflows), not at device names. Tailwind's default breakpoints are a starting set; move them if the content demands.
- Start from the narrow layout and enlarge (mobile-first utilities: `md:grid-cols-2`).
- Intrinsic grids need no breakpoints: `grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr))`.
- Use `min-w-0` on flex and grid children that hold text, or they will overflow.
- No horizontal page scroll at 320px wide. Wide tables scroll inside their own container.
- Use `100dvh` rather than `100vh` for full-height mobile layouts. Handle safe-area insets for fixed bars (`env(safe-area-inset-bottom)`).
- Use container queries (`@container`) for components that live in different widths, such as cards in a sidebar versus a main area.
- Fix the aspect ratio of images and embeds (`aspect-ratio`, `next/image` with dimensions) so layout does not jump while loading.
- Hover-only behaviour needs a touch equivalent. Guard hover styles with `@media (hover: hover)` if the Tailwind version does not already.
- Every multi-column layout states its small-screen fallback (single column below about 768px, recommended) in the same component. Check by resizing through 768 and 375.
- Prefer CSS grid over percentage `calc()` widths in flex rows.
- Fix the cause of horizontal overflow; do not hide it with `overflow-x: hidden` on the page root. Check: scrollWidth equals clientWidth at 320, 375 and 768.
- A tile or bento grid has exactly as many cells as content, with no empty tile. Do not use `grid-auto-flow: dense` to fill gaps; it reorders what is seen without reordering the DOM and breaks keyboard and reading order.
- Over about five list items, group, tabulate or disclose instead of a long bordered list (see `review-format.md` for the flag).
- Primary button labels fit on one line at desktop width; if one wraps, shorten the label or widen the button.
- One label per intent on a page: two buttons that do the same thing get the same words (see information-architecture).
- One theme per screen unless the design deliberately switches once. Scroll the full page in both themes for strays.
- Marketing pages only: do not repeat the same two-column image-and-text split more than twice in a row.

## Room for text expansion

Translated text is often longer than English, and user names and titles are unpredictable.

- No fixed widths or heights on elements that hold text; use `min-w-*`, `max-w-*`, and `min-h-*`.
- Buttons grow with their label; do not clip. Test with a label about 50% longer than the English one (recommended test value).
- Allow wrapping in labels, headings, and tabs unless truncation is deliberate and recoverable (see `typography-and-colour.md`).
- Layouts must survive a very long word, an empty value, and a single character.
- Do not build sentences from concatenated fragments; use whole translatable strings.

## State matrix

Every interactive element needs every state that applies. Fill this table for each component under review.

| State | Required treatment |
| --- | --- |
| Default | clear affordance: looks clickable or editable |
| Hover | subtle change (colour, background); pointer devices only |
| Focus-visible | visible indicator on keyboard focus; never `outline: none` without a replacement |
| Active (pressed) | immediate, stronger than hover; see `motion.md` |
| Disabled | reduced emphasis, `cursor: not-allowed`, no hover or press response, still legible; use the real `disabled` attribute |
| Loading | control stays the same size, shows progress, blocks repeat submits, announces to assistive tech |
| Empty | explains why nothing is shown and offers the next action |
| Error | says what went wrong and how to fix it, next to the cause, not by colour alone |
| Success | confirms the action completed; does not block the next step |

Rules:

- Use `:focus-visible` for keyboard rings and not `:focus`, so mouse clicks do not show the ring. The ring uses the accent token, stays at least 2px thick (recommended), has an offset, and is visible on both light and dark surfaces. Exact visibility thresholds: accessibility-review.
- Hover must not be the only way to reveal an action or information.
- States change appearance without changing size: no layout shift between default, hover, and loading. Use `ring` or `outline`, not border width changes.
- Disabled controls that need explanation show the reason in adjacent text; a disabled button with no explanation is a finding.
- Loading: prefer a skeleton that matches the final layout for content, and an inline spinner inside the control for actions. Keep the label or replace with a clear "Saving" text.
- Empty: the title says what is missing, one sentence says why or what to do, and one action. No illustration is required.
- Error: place field errors directly below the field, connect with `aria-describedby`, and move focus or the message into view on submit. Keep page-level errors at the top of the affected region.
- Check: render the component with Storybook, a test page, or props that force each state; screenshot all.

```html
<button class="bg-accent text-on-accent rounded-lg px-4 h-10
  hover:bg-accent/90 active:scale-[0.97]
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accent
  disabled:opacity-50 disabled:pointer-events-none
  transition-[background-color,transform] duration-150">
```

## Form visuals

- Label above the input, left-aligned, always visible. Placeholder text is a hint, not a label, and disappears on typing.
- One control height across the form (inputs, selects, buttons in a row share a height token, for example `h-10`).
- Group related fields; use a grid for short fields (city and postcode) and full width for long ones.
- Mark optional fields as "optional" instead of marking every required field with an asterisk, when most fields are required.
- Helper text sits below the input, in `muted`. Error text replaces or follows it, in `danger`, with an icon.
- Inputs show their boundary (border or background) at rest. An input with no visible edge is a finding.
- Keep the submit button aligned with the field edge, labelled with a verb that says what happens.
- Do not clear the user's input on error.
- Set the right `type`, `inputMode`, and `autocomplete` so mobile keyboards and autofill work.

## Touch-friendly hit areas

- The clickable area can be larger than the visible element; extend it with padding or a pseudo-element (`before:absolute before:-inset-2`) without changing visual size.
- Space between adjacent targets must be enough to avoid mis-taps.
- Icon-only buttons need an accessible name (`aria-label`) and a hit area, not just a 16px icon.
- Minimum target sizes and spacing exceptions come from WCAG 2.2 and platform guidelines; use the accessibility-review skill for exact sizes rather than restating them here.
- Overlapping hit areas of neighbours are a finding. Check in devtools by hovering with the element inspector.
