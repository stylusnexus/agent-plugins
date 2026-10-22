---
name: interface-polish
description: "Use when polishing or reviewing the visual details of a UI: spacing and layout rhythm, border radii, shadows and borders, typography, colour tokens, dark mode, motion and transitions, interaction states (hover, focus, active, disabled, loading, empty, error), form visuals, and responsive layout. Written for Next.js/React with Tailwind-style utility CSS."
---

# Interface polish

Make small, consistent refinements that clarify hierarchy and make interaction feel responsive, without adding decorative complexity or new dependencies.

## When to use

- A screen works but looks uneven: spacing, radii, shadows, type, or colour feel inconsistent.
- A component is missing states (hover, focus, disabled, loading, empty, error).
- Transitions feel abrupt, slow, or janky.
- A layout breaks at narrow widths, with long text, or in another language.
- Reviewing a pull request for visual quality.

Not for: exact contrast ratios, target sizes, screen-reader behaviour (use accessibility-review); information architecture (use information-architecture); full redesigns (use ui-ux).

## Guardrails

- Inspect the design system first. Use its tokens and components before writing new values.
- Add no runtime dependency for cosmetic effects. CSS and the utility framework already in the project are enough.
- Respect `prefers-reduced-motion`. Never rely on motion alone to convey meaning.
- Change only what the principle justifies. Do not restyle working areas outside the request.

## Workflow

1. **Inspect tokens.** Find the Tailwind config or CSS variables (colours, spacing, radii, shadows, fonts, durations). Note what exists. List raw values in the target code that bypass tokens.
2. **Audit.** Walk the target against the reference files below. Record each finding with a principle, a severity, and a file.
3. **Fix.** Apply the smallest change that resolves each finding, using tokens. Prefer one token change over many local overrides.
4. **Verify.** Render at 320px, 768px, and a wide desktop width, in light and dark themes. Tab through with a keyboard. Toggle reduced motion in the OS or browser devtools. Run typecheck and lint. Anything you cannot run goes under "Could not verify".

## Reference files

- `surfaces-and-spacing.md`: open for spacing scale, radii, shadows versus borders, icon alignment, dividers, density.
- `motion.md`: open for transitions, durations, easing, press feedback, enter/exit, reduced motion.
- `typography-and-colour.md`: open for type scale, line height, wrapping, numerals, truncation, colour tokens, dark mode.
- `layout-and-states.md`: open for grouping, alignment, responsive structure, the state matrix, form visuals, hit areas.
- `review-format.md`: open before writing the final report; it has the template, severity scale, and checklist.
- `style-presets.md`: open only when the product owners ask for a named look (soft, minimalist, brutalist). Optional; built from existing tokens.

## Output

Return the report in the format in `review-format.md`: a Before/After table grouped by design principle (columns Principle | Before | After | File), then severity-tagged findings not fixed, the filled checklist, and a "Could not verify" section. When code was changed, list every touched file.

## Boundaries

- Report-only unless asked to implement. A question about a design is a question; answer it.
- Values marked "recommended" in the references are defaults, not standards. If the design system has its own value, the design system wins.
- Do not rename tokens, reorganise files, or upgrade dependencies as part of polish.
- Style presets are optional and chosen by the product owners. Never restyle a screen into a preset unasked.
- Mention problems outside the scope in one line each; do not fix them.
