# Brand kit parts and the design rules behind them

**What's sourced and what isn't.** The color, type, and accessibility rules cite public standards, linked inline below. Assembling them into one small team's kit is this suite's own reasoning, labeled INFERENCE.

A brand kit works like a codebase's design tokens: fixed, checkable values (a hex code, a font name, a contrast ratio) instead of a felt impression like "roughly blue." Three parts need tokens this way: **color**, **type**, and the **name and logo** on top of them.

## Color: pick it, then prove it's legible

Before a palette is final, check every text-on-background pairing against the Web Content Accessibility Guidelines' contrast-minimum rule: normal text needs a ratio of at least 4.5:1, large-scale text (18pt+ regular, or 14pt+ bold) needs at least 3:1 — threshold values, so 4.499:1 does not pass (Source: W3C, WCAG 2.2, "Understanding Success Criterion 1.4.3: Contrast (Minimum)" — https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Logo/brand-name text is exempt from this rule, but an unreadable logo still fails its job (INFERENCE). Run every pairing through a contrast checker before locking a palette in, not after a design ships.

## Type: name a small set of roles, then pick fonts that hold up together

Decide what jobs type needs to do before picking fonts by eye. Material Design 3 names five roles — *display*, *headline*, *title*, *body*, *label* — display for short, high-impact text; body for long passages; label for small utilitarian text (Source: Google, Material Design 3, "Typography — Applying type" — https://m3.material.io/styles/typography/applying-type). A small team doesn't need all five, but naming two up front — heading and body — beats starting from zero each time.

Apple's HIG adds a rule worth carrying over regardless of platform: hierarchy comes from weight, size, and color together, not size alone, and very light weights are called out as less accessible (Source: Apple, Human Interface Guidelines, "Typography" — https://developer.apple.com/design/human-interface-guidelines/typography). Its color guidance applies the same logic: color supports meaning, never carries it alone — a status or error state still needs an icon or label, since color-blind readers can't rely on color (Source: Apple, Human Interface Guidelines, "Color" — https://developer.apple.com/design/human-interface-guidelines/color).

For pairing two fonts, Google Fonts points at structural similarity — x-height, stroke contrast, width — over two fonts that each look good alone; typefaces drawn from the same family or "superfamily" share that structure by construction, giving "enough contrast... to not require a pairing from another typeface" plus consistency across every variant (Source: Google Fonts, Fonts Knowledge, "Pairing typefaces within a family & superfamily" — https://fonts.google.com/knowledge/choosing_type/pairing_typefaces_within_a_family_superfamily, accessed 2026-09-24).

## Name and logo

A name and logo show up small, on dark backgrounds, in black-and-white print, next to other logos. None of the sources above certify a required-variant list — treat this as practice, not a rule: check the logo at its smallest realistic size and on both a light and a dark background before calling it final (INFERENCE).

## Design checks

A short list of checks a graphic can be judged against, each traceable to a source above rather than to taste:

- **Contrast** — the WCAG ratios above. The one principle with a hard, checkable number.
- **Hierarchy** — weight, size, and color together, not size alone.
- **Consistency** — a named type role and a brand color mean the same thing everywhere, not a per-screen choice.
- **Meaning independent of color** — a color signal always carries an icon or label too.
- **Fit for the setting** — a pairing that passes on a laptop still needs checking on a phone, in print, and small.

## Applying it

Record the result as a literal table: exact hex values, exact font names per role, and which pairings passed a contrast check, at what ratio. That table makes "on brand" checkable instead of a feeling.

A worked contrast-ratio example lives in the [brand kit canvas](../templates/brand-kit-canvas.md) template, not here — this reference file doesn't carry invented examples, only the sourced rule.
