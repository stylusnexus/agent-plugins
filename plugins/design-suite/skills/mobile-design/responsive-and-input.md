# Responsive layout and input

## 1. Mobile-first CSS

- Write base styles for the narrowest layout, then add complexity with `min-width` media queries. The single-column layout is the default, not the exception.
- Use content-driven structure: flexbox/grid with `minmax()`, `auto-fit`/`auto-fill`, wrapping, `gap`, instead of fixed widths.
- Use relative units for type and spacing (`rem`, `em`, `%`, `ch` for measure) so user text-size settings work.
- Do not disable zoom: never set `user-scalable=no` or `maximum-scale=1`.
- Set `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Container queries (`@container`) suit components that live in different-width slots. Use them where the codebase already supports them; do not add tooling for them.
- Reflow requirement: content usable at 320 CSS px width without two-dimensional scrolling, except data tables, maps, images where 2D layout is essential (WCAG 1.4.10).

## 2. Breakpoints driven by content

- Add a breakpoint where the layout breaks (lines too long, items cramped, columns too narrow), not at named device widths.
- Reuse the project's existing breakpoint tokens; adding more needs a reason. Typical widths in the codebase, if present, are the starting point; there is no standard set.
- Test continuous widths from 320 CSS px up, not only at the breakpoints, and at 200% text size. Spot-check 320 (reflow), 375, 390 and 768.
- Multi-column layouts collapse to one column below about 768px (recommended; the project's own breakpoint wins).
- Remove overlapping, rotated and negative-margin layouts on small screens; they cause touch collisions.
- Body text is 16px (1rem) or larger on mobile (recommended). Never shrink body text to make something fit.
- Primary actions may be full width on small screens.
- Vertical section spacing scales down with width using a fluid range (`clamp()`), not a fixed large gap.
- Avoid separate mobile and desktop DOMs that duplicate content; hidden duplicates confuse assistive technology and cost bytes.

## 3. Viewport units

| Unit | Meaning | Use |
|---|---|---|
| `vh` | Largest viewport height; on mobile browsers includes area behind collapsing toolbars | Can cause content to be hidden under browser UI |
| `svh` | Small viewport height; browser UI fully shown | Safe minimum for full-height layouts |
| `lvh` | Large viewport height; browser UI hidden | Backgrounds that may extend |
| `dvh` | Dynamic; follows the browser UI as it shows or hides | Full-height regions that should fit the visible area; layout may resize while scrolling |

Guidance: prefer `min-height: 100svh` or `100dvh` over `100vh` for full-screen sections; provide a `vh` fallback line before it for older browsers. Avoid `dvh` on elements that cause visible resizing during scroll (can look jumpy); `svh` is steadier. Do not size text with viewport units alone (breaks text scaling); combine with `clamp()` and rem.

## 4. Safe-area insets

On devices with notches, rounded corners and home indicators, fixed UI can sit under system areas.
- Opt in with `viewport-fit=cover` in the viewport meta only if drawing edge to edge is intended.
- Pad fixed bars with `env(safe-area-inset-top|right|bottom|left)`, for example `padding-bottom: max(12px, env(safe-area-inset-bottom))`.
- Applies to bottom tab bars, sticky action bars, full-bleed images with overlaid text, and landscape side edges.
- Test in landscape: insets move to the sides.

## 5. Forms and input

Type and attributes matter more on mobile because they select the keyboard and enable autofill.

| Data | Use |
|---|---|
| Email | `type="email"`, `autocomplete="email"`, `inputmode="email"` optional |
| Phone | `type="tel"`, `autocomplete="tel"` |
| URL | `type="url"` |
| Integers such as a code or PIN | `inputmode="numeric"` with `pattern="[0-9]*"`; keep as text so leading zeros survive |
| Decimal numbers | `inputmode="decimal"` |
| One-time code | `autocomplete="one-time-code"`, `inputmode="numeric"` |
| Search | `type="search"`, `enterkeyhint="search"` |
| Name | `autocomplete="name"` or `given-name` / `family-name` |
| Address | `street-address`, `postal-code`, `country` etc. |
| Passwords | `autocomplete="current-password"` or `"new-password"`; allow paste and password managers |
| Date | native `type="date"` where acceptable; otherwise a clearly formatted text field |

Also:
- Use `autocomplete` tokens for personal data fields (WCAG 1.3.5 Identify Input Purpose).
- `enterkeyhint` sets the keyboard action label (next, done, go, search).
- `autocapitalize`/`autocorrect` off for codes, usernames and emails.
- A visible `<label>` for each field, not placeholder only; placeholder disappears and is low contrast.
- Font size of inputs at least 16 px prevents automatic zoom on iOS Safari on focus (browser behaviour; verify on device).
- Do not ask for information already given earlier in the same process (WCAG 3.3.7 Redundant Entry).
- Authentication must not depend on a cognitive test such as memorising or transcribing; allow paste and password managers (WCAG 3.3.8).

## 6. Keyboard avoidance

- The on-screen keyboard covers roughly the lower half of the screen; the focused field and its error must stay visible.
- Scroll the focused input into view; keep primary action reachable (sticky submit above the keyboard, or place it after the last field).
- Use `visualViewport` or `interactive-widget=resizes-content` in the viewport meta where supported to size layout to the visible area; test on real devices because behaviour differs between browsers.
- Do not use fixed bottom bars that sit on top of the keyboard and hide fields.
- Move to next field with Next/enter key hints; submit on final Done.

## 7. Form length and flow

- Ask only what the task needs. Every field is a cost; list fields that can be removed, deferred, derived or defaulted.
- One column. Group related fields; break very long forms into steps with visible progress and saved answers.
- Validate on blur or submit with specific messages; avoid validating while the user is still typing the first characters.
- Preserve input on error, back, and rotation.
- Offer paste, autofill and device pickers instead of custom widgets where they fit.
- Required indication consistent and accessible (text, not colour alone).

## 8. Orientation

- Support both portrait and landscape; do not lock orientation unless essential (WCAG 1.3.4).
- Re-flow on rotation without losing state or scroll position.
- Check fixed headers/footers in landscape: short viewport height can leave little room for content.
- Check insets, on-screen keyboard height, and modals in landscape.

## 9. Acceptance checks (stated viewport)

- At 320 CSS px wide and 200% text: no clipped text, no sideways page scroll, all functions available.
- Each form field has a label, the right keyboard and appropriate autocomplete token.
- Fixed bars clear the safe area in both orientations.
- Focused fields are never hidden by the keyboard on a real device.
