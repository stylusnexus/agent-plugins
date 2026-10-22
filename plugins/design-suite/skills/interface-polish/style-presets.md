# Style presets

Ideas restated from the MIT-licensed [taste-skill-classics](https://github.com/Leonxlnx/taste-skill-classics) by Leonxlnx; not copied text.

Three optional, named looks. None is a default. For the full versions, with the draw step that picks a direction and the browser inspector that checks the result, use the art-direction skill.

- The product owners choose the preset. A reviewer may suggest one and must say why; never apply one unasked.
- A preset is built from the project's existing tokens and stack. Adopting one adds no fonts, no icon libraries and no motion libraries. If a preset calls for something the project lacks (a serif, a mono face), skip that part or list it as a product owner decision.
- Every colour pair a preset produces is checked with accessibility-review. Example hex values from other sources are not safe defaults; compute on the project's real colours.
- Numbers are "recommended", not standards. The design system's own values win.
- Motion level is stated in plain words (none, low, medium). Every preset respects `prefers-reduced-motion` and gives a static end state (see `motion.md`).
- Do not mix presets on one screen. Pick one theme per screen (see `layout-and-states.md`).

## Soft: calm, spacious, tactile

When it fits: consumer products and portfolio pages where a quiet, premium feel supports the content. Poor fit for dense tools.

- Palette logic: one accent. Either a very dark neutral with a faint tinted glow, warm light neutrals, or silver-grey and white. Separate surfaces with hairline edges at low opacity rather than grey borders. No heavy black shadows. A raised panel may sit in a thin outer shell (a tray holding a plate); inner corners stay concentric (see `surfaces-and-spacing.md`).
- Type logic: one confident sans for large headings, calm body text. Labels stay at 12px or larger.
- Spacing and density: low density, very large gaps between sections, large radii, pill buttons. A trailing icon may sit in its own small circle inside the button.
- Motion level: medium. Slow ease-out, small press scale, soft fade-up on entry, all gated by reduced motion.
- Avoid: blur on scrolling content (blur only on fixed bars and overlays), stacked blurs, text over glass without a measured contrast check, a floating nav that covers focused elements, grain on a scrolling container (grain, if used at all, goes on a fixed layer).

## Minimalist: editorial, document-like

When it fits: workspace tools and content products where the interface should read like a clean printed page.

- Palette logic: warm or plain white canvas, near-black text (not pure black), one hairline border colour. Colour is rare and means something. Muted tinted fills only for tags, with darker text of the same hue; check each ratio. No decorative gradients, no large coloured blocks.
- Type logic: neutral sans for the interface. A serif for large headings and quotes only, and only if the project already has one. Mono for shortcuts and metadata only if already present. Tight tracking and tight line height only at display size.
- Spacing and density: low to medium density, generous gaps. Tiles of unequal size with 1px borders and small radii (about 8-12px, recommended). Flat: no default shadows.
- Motion level: low. Gentle fade-up on entry, a tiny hover change, press scale. Any ambient background drift is optional and off under reduced motion.
- Avoid: pill-shaped large containers, heavy shadows, neon accents, emoji as decoration, thin low-contrast secondary text (secondary grey is the usual contrast failure).

## Brutalist: industrial, data-first, hard edges

When it fits: developer tools and telemetry views where visible structure and raw function are the point.

- Palette logic: choose exactly one base, either paper-like with near-black ink or dark with off-white text. One signal colour for alerts only. No gradients, no translucency. Check the signal colour as text on the base; a red that looks vivid often fails for small text.
- Type logic: large, compact display text against small, spaced labels. Uppercase through `text-transform`, not typed capitals. Labels stay at 12px or larger. Tabular figures for numbers.
- Spacing and density: rigid grid with visible 1-2px dividers. Swings between dense data blocks and large empty areas. No rounded corners.
- Motion level: none to low. Any flicker or scan effect is off under reduced motion and must not reduce legibility.
- Avoid: mixing light and dark in one interface; decorative ASCII or symbol framing that a screen reader will read aloud (hide it); scanline or noise overlays over body text; very tight line height on multi-line text; tracking so tight that glyphs touch.

## Using a preset in a review

1. Name the preset and the product owner decision that chose it, or write MISSING INFORMATION.
2. List which tokens carry it (palette, radius, shadow, motion duration). Add no new token families.
3. Run the usual checklist in `review-format.md`; the preset changes no rule there.
