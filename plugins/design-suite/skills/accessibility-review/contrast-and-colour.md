# Contrast and colour

Related criteria: 1.4.1, 1.4.3, 1.4.6 (AAA), 1.4.11, 2.4.7.

## Thresholds

| Criterion | Level | What | Minimum |
|---|---|---|---|
| 1.4.3 Contrast (Minimum) | AA | Text and images of text | 4.5:1 normal; 3:1 large |
| 1.4.6 Contrast (Enhanced) | AAA | Same | 7:1 normal; 4.5:1 large |
| 1.4.11 Non-text Contrast | AA | UI component boundaries/states needed to identify them, and graphics needed to understand content | 3:1 against adjacent colors |
| 1.4.1 Use of Color | A | Color is not the only way to convey information | Add a second cue |

Ratios are not rounded: 4.499:1 fails 4.5:1.

Large text: at least 18 point (24 CSS px) regular, or at least 14 point (about 18.66 CSS px) bold. Everything else is normal. Body text, labels, helper text, and captions are normal text; Tailwind `text-sm`/`text-xs` are always normal.

A rule written as "large text is 18px and up" is wrong: 18px regular is normal text and needs 4.5:1.

Exempt from 1.4.3 and 1.4.11: disabled (inactive) controls, pure decoration, logos and wordmarks, text that is incidental in a photo. Do not treat "disabled looking" as an excuse for an enabled control, and note that low-contrast disabled text still hurts comprehension; mention as Minor if it carries meaning.

## How to compute

Relative luminance from sRGB 0-255 channels:
```
c = channel / 255
lin = c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4
L = 0.2126*R_lin + 0.7152*G_lin + 0.0722*B_lin
ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```
```js
const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
const lum = ([r, g, b]) => 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
```
Reference points to sanity-check a script: black on white is 21:1; #767676 on white is about 4.54:1 (the lightest neutral grey that passes 4.5:1 on white).

Alpha: composite the foreground over the real backdrop first (`rgba` or Tailwind `text-black/60`, `bg-white/10`), then compute. A semi-transparent color has different contrast on every background it appears over.

Tools already available without installing: browser DevTools color picker (shows ratio and AA/AAA marks), Lighthouse/axe in DevTools, a short script like the one above. If none is possible, label the finding NEEDS-TEST and give the computed estimate with the formula inputs.

## What to check in the source pass

1. Design tokens: list each text/background pair actually used (body on page, muted on card, link on page, button label on button, placeholder on input, badge text on badge). Compute each in light and dark.
2. Tailwind utilities that commonly fail on white: `text-gray-400` and lighter, `text-slate-400`, `placeholder:text-gray-400`, `text-blue-400`. Verify against the project's actual palette rather than assuming; palettes are customizable.
3. Hover/active/visited/selected states: contrast is needed in each state, not only the default.
4. Brand color on tinted surfaces (`bg-blue-50` plus `text-blue-500`) is a frequent miss.
5. Every button label against its fill: accent fills, ghost buttons over photos, and hover states. Also check placeholder, helper text, error text and focus rings, not only labels.
6. Saturated mid-tone accents with white text often fail. Worked examples, computed on sample colours (recompute on the project's real colours): white on emerald #10B981 is 2.54:1, on amber #F59E0B 2.15:1, on blue #3B82F6 3.68:1, on rose #E11D48 4.7:1 (the only one that passes 4.5:1).
7. Secondary and tertiary grey text is a common failure. Worked examples, same caveat: #787774 on white is 4.48:1 and on #F7F6F3 is 4.14:1; #94A3B8 on white is 2.56:1; a red #E61919 as text is 4.22:1 on #F4F4F0 and 4.26:1 on #0A0A0A. All fall below 4.5:1 for small text.

## Non-text contrast (1.4.11)

Needed at 3:1 against the adjacent background:
- Boundary of a text input, select, checkbox, radio, or toggle track when the boundary is what identifies the control. A light-grey 1px border on white commonly fails. If the control has a visible label and a filled background that already meets 3:1, the border is not required.
- Icon-only buttons: the icon glyph itself (it is the identifier).
- Focus indicator (see `keyboard-and-focus.md`), against both the component and the page.
- State indicators: checked checkmark, selected tab underline, toggle knob vs track, slider thumb and track.
- Charts: data marks, lines, and segment boundaries needed to read the data; legend swatches. Add direct labels or patterns so color identity is not the only carrier.
Not required: the text-less shape of a button that has a text label with sufficient contrast, or inactive components.

## Use of colour (1.4.1)

Information carried by color needs a second cue: text, icon, pattern, underline, position, or shape.
- Links inside body text: underline them, or provide at least 3:1 contrast against surrounding text plus a non-color cue on focus and hover. Underline is the simple fix.
- Form errors: red border alone fails; add an icon plus message text (see `forms-and-errors.md`).
- Status badges and chart series: text label, icon, or pattern.
- Required fields: asterisk or text "required", not color.
- Instructions like "click the green button" need another identifier.
Check by viewing the page in grayscale (DevTools rendering emulation: vision deficiencies, achromatopsia) to confirm meaning survives.

## Placeholder text

Placeholder text that carries the label or an example is text and needs 4.5:1. Browser default placeholder color often fails; Tailwind `placeholder:text-gray-400` on white fails with its default palette. Do not use placeholder as the label: it vanishes on input and is not a dependable accessible name (3.3.2; see `forms-and-errors.md`). Put hints in persistent helper text.

## Text over images and gradients

- Contrast is measured against the worst-case pixel behind the text in the relevant region, not the average. Test at several viewport widths since crops move.
- Reliable approaches: a solid or scrim layer behind text (`bg-black/60` over a known image must be computed against the image's lightest area), text on a solid panel, or text outside the image.
- Text-shadow may help but is not a substitute for measurement.
- User-uploaded or CMS images: you cannot guarantee contrast; require a scrim or panel and mark as NEEDS-TEST.
- Frosted glass and blur surfaces: provide a solid fallback for users who reduce transparency (`prefers-reduced-transparency`; browser support is uneven, so test), and measure contrast against the worst background beneath.

## Dark mode and themes

- Check every theme separately; a passing light palette says nothing about dark. Flipped tokens (`text-gray-400` on `bg-gray-900`) often pass but `text-gray-600` on `bg-gray-800` fails.
- Pure white on pure black produces glare for some users, but the criterion is only the ratio; mention glare as a Minor design note if raised, not a failure.
- Focus rings, borders, charts, and shadows (shadows convey nothing in dark mode) need their own dark tokens.
- Honor `prefers-color-scheme` or a user toggle; if a toggle exists, it must be keyboard-operable and the choice persisted. Set `color-scheme` so native controls and scrollbars follow.
- `prefers-contrast: more` and `forced-colors: active` are worth supporting: do not use background images or box-shadows as the only carrier of borders; use `border` or `outline`, which forced-colors maps to system colors. In forced colors, use system colors (`CanvasText`, `Highlight`) rather than hard-coded values.

## Reporting a contrast finding

Give: element and location, foreground and background (hex, after alpha compositing), computed ratio, required ratio, text size class (normal or large), state, theme. Fix: the nearest token that passes, with its ratio. Example: "`text-gray-400` (#9ca3af) on `bg-white`: 2.5:1, needs 4.5:1; use `text-gray-600` (#4b5563), 7.6:1." Always recompute rather than trusting this example if the palette differs.

## Compute, do not estimate

From this skill's folder, `python3 scripts/contrast.py '#767676' '#ffffff'` prints the ratio and whether it passes each WCAG level. It also reads colour custom properties from a CSS file (`--css app.css --pair text:surface`). It exits 1 when a pair misses AA for normal text, so it can gate a check. It measures the two colours you give it; text over an image, gradient or translucent layer still needs its own measurement.
