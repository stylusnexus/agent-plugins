# Surfaces and spacing

Rules for space, corners, depth, and separation. Check the design system's tokens before using any value here; the numbers are recommended defaults.

## Spacing scale

- Use a 4px base unit (recommended). Tailwind's default scale is built on 4px steps (`p-1` = 4px, `p-2` = 8px, `p-4` = 16px), so most work needs no custom values.
- Pick spacing from a short set: 4, 8, 12, 16, 24, 32, 48, 64. Arbitrary values (`p-[13px]`) are a finding unless they correct an optical issue, and then they need a comment.
- Space inside a group is smaller than space between groups. If the two are equal, grouping is lost (see `layout-and-states.md`).
- Use `gap` on flex and grid parents instead of margins on children. Margins on children break when items wrap or reorder.
- Check: list every distinct padding and gap value in the file. More than about six distinct values usually means the scale is not being followed.

```html
<!-- Before: mixed values -->
<div class="p-[14px] space-y-[9px]">
<!-- After: scale values -->
<div class="p-4 flex flex-col gap-2">
```

## Concentric radius

When a rounded element sits inside a rounded container, the outer radius equals the inner radius plus the padding between them.

```
outer radius = inner radius + padding
```

- Card with `p-4` (16px) holding a button with `rounded-lg` (8px): the card needs 8 + 16 = 24px, which is `rounded-3xl`.
- With a CSS variable: `border-radius: calc(var(--inner-radius) + var(--pad))`.
- If padding is larger than the inner radius, corners look uneven even when the sum is right. Keep nested padding at or below about 16px for rounded children, or drop the inner radius.
- Use one radius per role (control, card, modal, pill) and keep it consistent across the app. Do not mix `rounded-md` and `rounded-lg` for the same role. Write the scale down (for example buttons pill, cards 16px, inputs 8px; recommended illustration only).
- Check: list the distinct radius values on a screen; each must map to a named role.
- Check: nested rounded boxes where inner and outer radii are equal. That is the usual bug.

## Optical alignment of icons

Geometric centring is not always visual centring.

- Icons with weight on one side (play triangles, arrows, chevrons) look off-centre when mathematically centred. Shift them 1-2px (recommended) toward the pointed or lighter side, so the visual mass, not the bounding box, sits in the middle. A play triangle moves right.
- In a button with an icon and a label, the icon's visual edge should sit nearer the edge than the label's side. Reduce padding on the icon side by about 2-4px (recommended) so the button does not look heavy at that end.
- Align icon height to the text's cap height or line height, not to the font's full box. In flex rows use `items-center` and give the icon the same size as the line height (`size-5` next to `text-sm/5`).
- Use one icon size per context (for example 16px inline, 20px in controls, 24px standalone). Do not scale icons by eye.
- Stroke width must match across the icon set in one view.

## Elevation: shadows versus borders

- Borders express structure: tables, lists, inputs, sections that sit on the same plane.
- Shadows express layers that float above the page: menus, popovers, dialogs, toasts, dragged items. If an element does not float, it does not need a shadow.
- Do not use both a heavy border and a heavy shadow on the same element. Choose one signal.
- Cards that sit in a page: a 1px border in a low-contrast border token, or a very faint shadow. Not a large blurred shadow.
- Use a card only when raised height means something. Test: remove the card's border and shadow; if the grouping still reads, the card was decoration, so use a divider or space instead.
- Pick border-led (flat) or shadow-led (raised) per surface. A 1px grey border plus a heavy drop shadow doubles the edge and looks muddy.

### Layered shadows

A single large shadow looks smudged. Stack two or three (recommended): a tight, darker one for contact, a wider, fainter one for lift.

```css
--shadow-floating:
  0 1px 2px rgb(0 0 0 / 0.08),
  0 4px 8px rgb(0 0 0 / 0.06),
  0 12px 24px rgb(0 0 0 / 0.06);
```

- Shadow colour should be a low-opacity version of a dark neutral tinted toward the surface hue, not pure black at high opacity. On light surfaces keep each layer's alpha at or below about 0.08 (recommended).
- Y offset larger than blur radius looks detached. Keep blur at least as large as the offset.
- Higher elevation means larger offset and blur, not darker colour. Define 3 or fewer elevation tokens (resting, raised, overlay).
- Dark mode: shadows show little on dark surfaces. Raise elevation with a lighter surface token and a subtle border, not a heavier shadow.

## Avoiding heavy borders

- Prefer 1px borders at low contrast against the surface. A 2px border signals focus or selection, not structure.
- Do not box everything. If spacing and alignment already group items, remove the border.
- Between stacked list rows use a divider on one side only, and none after the last row (`divide-y`, or `last:border-b-0`).
- Borders and radii: borders follow the curve, so check corners at small radii for thickness pinching.
- Selection and focus use a ring (`ring-2`) or outline, which does not shift layout, rather than changing border width.

## Outlines on images

Images on a surface of similar tone (a pale photo on a white card, a dark cover on a dark theme) lose their edge.

```css
.avatar, .cover {
  outline: 1px solid rgb(0 0 0 / 0.1);
  outline-offset: -1px; /* draws inside the image box, no layout shift */
}
/* dark theme: use a light edge */
:root[data-theme="dark"] .avatar { outline-color: rgb(255 255 255 / 0.1); }
```

- Use `outline` with negative offset, not `border`, so image dimensions stay unchanged.
- Apply to avatars, album covers, thumbnails, and any image with unpredictable edge tone. Skip full-bleed hero images.

## Dividers

- Use a divider only when whitespace is not enough to separate content.
- Use a border token, 1px, never pure black or pure white.
- Inset dividers inside lists to align with the text edge, not the container edge, when rows have leading icons or avatars.
- Use `<hr>` or `role="separator"` for true thematic breaks; decorative lines can be a border.

## Density

- Define at most two density levels (default and compact) and apply them through tokens (row height, padding), not per-component overrides.
- Compact density shrinks padding and row height, not text below a readable size and not hit areas below the minimum (see `layout-and-states.md`).
- Dense data tables: keep line height and cell padding consistent in every column; align numbers right with `tabular-nums`.
- Do not mix densities within one list or table.

### Section spacing bands

Name the band in the review, then check spacing is uniform inside it. Bands: airy (very large gaps between sections), ordinary app (moderate), dense (tight, hairline dividers). Check: vertical gaps between sibling sections take one or two values only. The band comes from the design system, not from taste.

## Layering and overlap

- Z-index is for named layers only (sticky nav, overlay, modal, tooltip). Keep the scale in one place. Check: no z-index value outside the documented scale.
- Do not overlap content on content with absolute positioning to fake depth; it collides at other widths and causes touch conflicts. Check at 375, 768 and 1440: no text box intersects another text box or an image.
