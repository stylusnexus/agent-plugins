---
name: mk-brand-kit
description: "This skill should be used when the user asks for a brand kit, product voice, a palette, fonts, a logo system, visual consistency, brand guidelines, or which design tool to use for a marketing asset."
---

A brand kit turns "roughly blue" and "sounds about right" into fixed, checkable values: exact hex codes, named font roles, a documented voice — the same idea as a codebase's design tokens, applied to how a product looks and sounds instead of how it runs.

## When to use this skill

Building or reviewing a color palette, a type system, a logo, a product's own voice (as distinct from the company's general house style), or deciding which tool — a template design tool, a product design tool, or code — should produce a given marketing asset.

## Workflow

1. **Define color and type as tokens, not impressions.** Check every text-on-background color pairing against WCAG 2.2's contrast-minimum rule (4.5:1 for normal text, 3:1 for large text) before locking a palette in. Name a small set of type roles — heading and body is enough for a small team — before picking fonts by eye, and pair fonts from the same family or superfamily when possible for built-in structural consistency. Full sourcing in [brand kit parts and the design rules behind them](references/brand-anatomy-and-design-principles.md).
2. **Judge any single graphic against the design checks**, not taste: contrast (the one with a hard number), hierarchy from weight/size/color together, consistency (a type role or brand color means the same thing everywhere), meaning that never rides on color alone, and fit for the actual setting it will appear in — same reference file.
3. **Record the result as a literal table**, not a mood board: exact hex values, exact font names per role, which pairings passed a contrast check and at what ratio. Use the [brand kit canvas](templates/brand-kit-canvas.md) to capture it. That table is what makes "on brand" checkable instead of a feeling.
4. **Draft a product voice sheet once the house floor exists.** A company-wide style guide doesn't say how one product's voice differs from another's or from a founder's personal writing. Pull do/don't word lists and before/after rewrites from real existing copy and real audience language (`mk-audience`, where available) — never from an adjective brainstorm or a competitor's tone. Method and the check against the house floor: [product voice sheet method](references/product-voice-sheet-method.md); capture it with the [product voice sheet](templates/product-voice-sheet.md). Mark it `HUMAN DECISION REQUIRED` until an owner approves it, and never overwrite the shared house style file directly.
5. **Route each asset to the right tool.** A template-based design tool for marketing images (social cards, OG previews, launch graphics) once real tokens exist to feed it; a product design tool for UI and engineering handoff; code for anything that must live in git and regenerate from data (README banners, generated OG images). Full routing logic, including how to connect a design tool that isn't connected yet, in [tool routing](references/tool-routing.md).

## Routing to sibling skills

- `mk-audience` — for the real audience language a product voice sheet's "do" words should be pulled from.
- `mk-copy` — the brand kit's voice and visual tokens are what copy gets checked against once both exist.
- `mk-founder-content` — for keeping a founder's personal voice distinct from any one product's voice.
- `marketing-lead` — for whether a full brand kit is worth the hours right now versus a narrower fix.

## Outputs

A filled [brand kit canvas](templates/brand-kit-canvas.md) with real hex values, font roles, and contrast-check results. A filled [product voice sheet](templates/product-voice-sheet.md) for one product, marked `HUMAN DECISION REQUIRED` until approved. A tool recommendation (template tool / product design tool / code) for a specific asset, with the reasoning from [tool routing](references/tool-routing.md).

## Adaptable prompt

"Build a brand kit canvas for [product]: propose a palette that clears WCAG contrast for [background color], name heading/body font roles with fonts that pair well together, and run each pairing through a design check. Then draft a product voice sheet against our house style using real copy from [where the copy already lives]."
