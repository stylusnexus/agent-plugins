# Touch targets and navigation

## 1. Touch target size

| Source | Value | Status |
|---|---|---|
| WCAG 2.2 SC 2.5.8 Target Size (Minimum), level AA | at least 24 by 24 CSS px, or enough spacing so a 24 px circle centred on the target does not overlap another target | Web minimum |
| WCAG 2.2 SC 2.5.5 Target Size (Enhanced), level AAA | at least 44 by 44 CSS px | Stricter optional level |
| Apple Human Interface Guidelines | 44 by 44 pt minimum | Platform guidance |
| Material Design | 48 by 48 dp minimum | Platform guidance |

Recommended for this suite: design primary touch controls to 44 to 48 px in the smaller dimension; treat 24 px as the floor for web, only where space forces it (dense tables, inline links in text). Inline links within a sentence are exempt from 2.5.8, but keep adequate line spacing.

How to get there without growing visuals: pad the hit area beyond the icon (padding or pseudo-element), keep the tappable box rectangular and unobstructed, and do not let a 16 px icon be its own target.

## 2. Spacing between targets

- Keep neighbouring targets separated so mis-taps are unlikely. Recommended: at least 8 px between adjacent targets (a design default, not a standard), more for destructive actions.
- Separate destructive controls from frequent ones; never place Delete next to Save with equal weight.
- Do not stack tiny controls in a row (icon toolbars) without checking each meets the target size.

## 3. Thumb reach (recommendation, not a measurement)

On large phones held in one hand, the top of the screen and the opposite corner are harder to reach than the lower middle. Recommended practice: put frequent primary actions in the lower part of the screen (bottom bar, sticky action area), keep destructive or rare actions away from the easiest reach zone, and avoid requiring top-corner taps for primary steps. Hand size, grip and device vary; reach is unknown for this product's users until measured. Mark audience posture as MISSING INFORMATION if the design depends on it.

## 4. Navigation patterns

| Pattern | Good when | Cautions |
|---|---|---|
| Bottom tab bar | 3 to 5 top-level destinations of equal importance used often (recommended range; platform guidance commonly aligns) | Always show labels with icons; keep active state obvious; do not use for actions; do not exceed 5 |
| Drawer / hamburger | Many destinations, infrequent use, secondary navigation | Hides options so discoverability drops; label the button "Menu"; consider using it for secondary items only |
| Top app bar with back | Hierarchical drill-in screens | Title says where you are; back goes up one level |
| Segmented control / tabs in page | Switching views of the same content | Keep to a few; do not nest tab bars |
| Search-first | Large catalogs | Provide recent items and scoped search; do not replace all browsing |
| Bottom sheet | Short contextual choices, filters | Must be dismissable, keyboard operable, and not trap focus without an exit |

Choose by number of destinations and frequency, not fashion. If more than 5 frequent destinations exist, review the information architecture before choosing a pattern (see information-architecture).

Keep navigation in the same place on every screen; indicate the current location; avoid hiding the only route to a core task behind a drawer.

## 5. Back behaviour

- Back moves up or back one step in the user's history and does not discard entered data without warning.
- On the web, the browser or system back must work: each meaningful screen has its own URL or history entry; modals and filters that users consider "a place" push history or can be dismissed with back.
- Never trap the user: no redirect loops, no overlay that ignores back.
- After completing a flow, back must not return to a stale submitted form; go to the result.
- Deep links open with a sensible back path (up to the parent, not exit).
- On gesture-navigation devices the edge swipe is back; do not place conflicting horizontal swipes at the screen edge.

## 6. Gestures always need a visible alternative

- Swipe, long-press, pinch, drag, double-tap and shake are not discoverable. Every action reachable by gesture must also be reachable by a visible control (button, menu).
- WCAG 2.2: SC 2.5.1 requires a single-pointer alternative for multipoint and path-based gestures; SC 2.5.7 requires a non-dragging alternative to dragging movements (reorder with move up/down buttons).
- Do not use gestures for destructive actions without confirmation or undo.
- Avoid conflicts with system gestures (edge swipes, pull-to-refresh on scrollable content inside a scroll view).
- Hover is not available on touch; show tooltip content some other way. Any information or control reachable only on hover is a defect.
- Horizontal strips need an affordance: part of the next item visible, snap points, and keyboard reachability.
- Long-press menus are accelerators only.

## 7. Text and content

- Support text scaling to 200% with no loss of content or function (WCAG 1.4.4); avoid fixed-height containers for text.
- Truncation is a last resort; provide the full text on open. Wrap by default.
- Keep line length comfortable on narrow screens; avoid horizontal scroll for text (WCAG 1.4.10 reflow at 320 CSS px width).
- Long tables: reshape into stacked cards or allow a contained horizontal scroll with sticky identifying column; never scroll the whole page sideways.

## 8. Review checks

- Measure each tap target at the narrowest supported width.
- List every gesture and its visible alternative.
- Walk back from each screen; note data loss and loops.
- Check one-handed reach for the top three actions, noting unknown posture.
