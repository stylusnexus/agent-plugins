# Typography and colour

Use the design system's type and colour tokens first. Numbers here are recommended defaults unless marked as a standard.

## Type scale

- Use a small fixed scale (about 6-8 sizes) from tokens: Tailwind `text-xs` through `text-4xl` is enough for most products. A new size needs a reason.
- Each step differs enough to read as a different level. Two sizes within 1-2px of each other look like a mistake.
- Limit weights to two or three (for example 400, 500, 600). Hierarchy should come from size, weight, and colour together, not weight alone.
- Body text: 14-16px on web (recommended); 16px for long reading. Do not go below 12px for any text a user must read.
- Use `rem`, not `px`, for font sizes so browser text-size settings work.
- Squint test: blur the screen; the order of importance should survive at similar sizes. The first heading should not shout; lean on weight and colour before scale.
- Negative letter-spacing (about -0.02 to -0.04em, recommended) is for display text only. Check: none below about 24px, none on body or small text.
- Emphasise a word with weight or italic of the same family, not a second typeface mid-headline.
- Italic display text needs descender room: line height at least 1.1 and a little bottom padding so g, y, p, q, j are not clipped.
- Serif only with a stated reason (editorial, publication, heritage), and not in dense software UI or dashboards. The brand brief decides.
- If fonts are already self-hosted, use `font-display: swap` and reserve space to limit layout shift. Do not add or link a font as part of a polish pass.

## Line height

- Body: about 1.5 (recommended). Tailwind `leading-normal` is 1.5; `leading-relaxed` is 1.625.
- Headings: tighter, about 1.1-1.3 (recommended). Large display text can go lower; check descenders and ascenders do not collide across wrapped lines.
- Small text (12-13px) needs slightly more line height, about 1.5, not less.
- Set line height unitless (`1.5`), not in px, so it scales with the font.
- WCAG 2.2 requires content to remain usable when users override line height to 1.5 times the font size and letter spacing to 0.12 times (Success Criterion 1.4.12). Do not use fixed-height boxes that clip text.

## Measure

Keep lines of body text roughly 45-75 characters. Use `max-w-prose` or `max-w-[65ch]` on text containers. Wide screens do not mean wide paragraphs. Tables, code, and UI chrome are exempt.

## Wrapping

```css
h1, h2, h3, .title { text-wrap: balance; }   /* even line lengths, short headings */
p, li, .description { text-wrap: pretty; }   /* avoids a single orphan word on the last line */
```

- Tailwind: `text-balance`, `text-pretty`.
- `balance` is for short text (headings, captions, callouts, empty-state titles). Browsers limit how many lines it applies to, so do not use it on long paragraphs.
- `pretty` is for body text. It is a progressive enhancement; unsupported browsers fall back to normal wrapping with no harm.
- Do not use `<br>` or hard-coded line breaks in headings to control wrapping; translated text will break.

## Tabular numerals

Numbers that change or stack in columns should not shift width as digits change.

```css
.metric, td.num, .timer { font-variant-numeric: tabular-nums; }
```

- Tailwind: `tabular-nums`.
- Use on counters, timers, prices in lists, table number columns, scores, dice totals, and progress percentages.
- Right-align number columns. Pair with `slashed-zero` or `diagonal-fractions` only if the product needs them.
- Check that the chosen font supports tabular figures; if not, the property has no effect.
- Do not use on running text, where proportional figures read better.

## Font smoothing

`-webkit-font-smoothing: antialiased` (Tailwind `antialiased`) affects macOS only and makes light-on-dark text look slightly thinner. Apply it once at the root if the design wants it; other platforms ignore it. It does not fix poor contrast. Do not set it per component.

## Truncation and clamping

- Single line: `truncate` (`overflow: hidden; text-overflow: ellipsis; white-space: nowrap`). In a flex child, add `min-w-0` or the text will not shrink.
- Multi-line: `line-clamp-2` (or 3). Use a clamp count that shows enough to be useful.
- Truncated text must stay reachable: provide the full value in a `title`, tooltip, expanded view, or detail page. Never truncate text that is the only way to identify an item (names in a list should wrap or expand).
- Do not truncate in a way that hides the end that carries meaning (file extensions, ID suffixes); truncate in the middle or put the key part first.
- Long unbroken strings (URLs, hashes): `break-words` / `overflow-wrap: anywhere`.

## Semantic colour tokens

Components should reference roles, never raw colours.

| Token | Role |
| --- | --- |
| `surface` | page and card backgrounds (with a raised variant) |
| `text` | primary text |
| `muted` | secondary text, captions, placeholders |
| `border` | dividers and control outlines |
| `accent` | primary action, links, selection, focus ring |
| `danger` | destructive actions, errors |
| `success` | confirmations, positive status |

```css
:root {
  --surface: #ffffff;  --text: #1c1c1e; --muted: #5f6368;
  --border: #e3e5e8;   --accent: #2f5bea; --danger: #c62828; --success: #1b7f3b;
}
```

- Check: no hex, `rgb()`, or `bg-blue-500` in component files when a role token exists. Add a token before adding a one-off colour.
- A warning role is useful but optional; add it only if the product uses it.
- Never convey status by colour alone. Pair it with an icon, text, or shape.
- Name tokens by role, not by value (`--accent`, not `--blue`).
- One accent, used for one job and identical everywhere. No new accent hue appears in a late section or footer badge. Check: distinct hue families on interactive or emphasis roles = the accent plus semantic state colours.
- Do not mix warm and cool neutrals on one screen. Check: sampled greys share a hue direction.

## Contrast pairing rules

Pair tokens, then verify the pair. Exact ratios and thresholds belong to the accessibility-review skill; use it for the numbers.

- Text on its intended surface: `text` on `surface`, `muted` on `surface`, `accent` text on `surface`. Verify each pair in light and dark.
- `muted` is the token most often too faint. Check it on every surface it appears on, including raised and hovered surfaces.
- Text on an accent or danger fill needs its own foreground token (`on-accent`), checked separately. Do not assume a saturated mid-tone accent takes white text. Worked example (checked on sample colours, recompute on the project's real colours): white on emerald #10B981 is 2.54:1, on amber #F59E0B 2.15:1, on blue #3B82F6 3.68:1; all fail 4.5:1 for normal text. Details: accessibility-review `contrast-and-colour.md`.
- Placeholder text, disabled text, and borders of inputs each have their own contrast requirements; send them to accessibility-review.
- Do not place text over images or gradients without a scrim or a checked solid backing.
- Focus indicators must be visible against both the element and its background.

## Dark mode tokens

Do not invert colours with a filter or flip values mechanically. Define a second set of tokens.

```css
:root[data-theme="dark"] {
  --surface: #121315; --text: #e8e9ea; --muted: #a0a4a8;
  --border: #2b2d31;  --accent: #7c9cff; --danger: #ff8a80; --success: #6fcf8e;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { /* same values */ } }
```

- Accent and status colours usually need to be lighter and slightly less saturated on dark surfaces than on light.
- Elevation in dark mode uses lighter surfaces, not stronger shadows (see `surfaces-and-spacing.md`).
- Images and illustrations with white backgrounds need a treatment (outline, container, or alternate asset).
- Support the system preference and, if the app offers a toggle, an explicit override. Apply the theme before first paint to avoid a flash.
- Check: every screen in both themes, including empty, error, and loading states.

## Avoid pure black on pure white

`#000` text on `#fff` is the highest possible contrast and can look harsh over long reading. A softer pair (recommended), such as near-black text (`#1c1c1e` to `#222`) on white or a very light grey, usually reads more comfortably while still passing contrast. The same applies in dark mode: avoid `#fff` on `#000`; use off-white on a very dark grey. Confirm the softer pair with the accessibility-review skill; softer is never an excuse to fall below the required ratio.
