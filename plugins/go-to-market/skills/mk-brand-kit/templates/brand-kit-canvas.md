# Brand kit canvas

Fill-in form derived from [brand kit parts and the design rules behind them](../references/brand-anatomy-and-design-principles.md). Fixed, checkable values only — a hex code, a font name, a measured contrast ratio, not a felt impression. Delete instruction lines (in *italics*) once filled.

## Color

| Role (e.g. background, body text, accent, button) | Hex value | Paired against | Contrast ratio (measured) | Passes WCAG? (4.5:1 normal text / 3:1 large text) |
|---|---|---|---|---|
| | | | | |
| | | | | |

*Run every text-on-background pairing through a contrast checker before locking the palette in — 4.499:1 does not pass. Logo/brand-name text is exempt from the ratio rule, but an unreadable logo still fails its job.*

## Type

*Name the roles this team actually needs — two (heading, body) is enough for a small team; don't fill in roles that won't be used.*

| Role | Font name | Weight(s) used | Notes |
|---|---|---|---|
| Heading | | | |
| Body | | | |

- **Pairing check:** *are the heading and body fonts from the same family or superfamily? If not, what structural similarity (x-height, stroke contrast, width) justifies the pairing?* →

## Name and logo

- **Logo file(s) / variant(s):** →
- **Checked at smallest realistic size?** → Y/N
- **Checked on both a light and a dark background?** → Y/N
- **Checked in black-and-white / print, if relevant?** → Y/N

## Design checks

*Run any finished graphic against these before calling it final — see the reference file for what each one traces back to.*

- [ ] Contrast — meets the WCAG ratio above.
- [ ] Hierarchy — comes from weight, size, and color together, not size alone.
- [ ] Consistency — this type role and this brand color mean the same thing everywhere, not a per-screen choice.
- [ ] Meaning independent of color — any color signal also carries an icon or label.
- [ ] Fit for the setting — checked on a phone and in print, not just on the screen it was designed on.

## Ownership

- **Who approves changes to this canvas?** →
- **Where does the approved version live?** →

---

### Example (fictional)

*Illustrative only — a made-up product, no real palette.*

A two-person team building a scheduling app for local service businesses tests a dark-teal-on-off-white palette. Body text at #1A4D4A on #FAFAFA measures 9.13:1, well past the 4.5:1 minimum. A lighter teal accent (#3E8C87) on the same background only measures 3.79:1 — below the 4.5:1 normal-text minimum — so they darken it to #2A6D68 (5.77:1) before it reaches button text. (Ratios computed with the WCAG relative-luminance formula, https://www.w3.org/TR/WCAG21/#dfn-relative-luminance.)
