# Motion

Motion explains change: what appeared, what left, what was pressed. If it explains nothing, remove it.

Every animation gets a one-sentence reason: it shows hierarchy, shows sequence, confirms an action, or shows a state change. "Looks nice" is not a reason; drop the animation. In a review, write the reason next to each animation in the diff. State the screen's motion level in plain words (none, subtle, medium). If the stated level cannot be built cleanly, lower the level; half-built motion is worse than none.

## Duration by purpose (recommended)

| Purpose | Duration |
| --- | --- |
| Press feedback (button down, toggle) | about 100-150ms |
| Small state change (hover colour, checkbox, tooltip) | about 150-250ms |
| Larger enter or exit (dialog, drawer, popover, page section) | about 250-400ms |

- Above about 400ms, interface motion usually feels slow. Reserve longer for deliberate, rare moments.
- Distance matters: a small element moving a short way is faster than a panel crossing the screen.
- Exits are shorter than enters (see below).

## Easing

- Entering: `ease-out` (starts fast, settles). The element arrives and responds immediately.
- Leaving: `ease-in` (starts slow, accelerates away).
- Moving between two on-screen positions: `ease-in-out`.
- Avoid `linear` except for continuous things (spinners, progress, marquees).
- Browser built-in `ease` is acceptable for small hover changes. A custom curve is a recommended refinement for larger movement.

```css
:root {
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);   /* recommended, entering */
  --ease-in: cubic-bezier(0.64, 0, 0.78, 0);    /* recommended, leaving */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1); /* recommended, moving */
}
```

If the design system defines easing tokens, use them instead.

## Exits shorter than enters

A user who dismisses something wants it gone. Make the exit about 60-75% of the enter duration (recommended): enter 300ms, exit 200ms. Do not block input while an exit animation plays.

## Animate only transform and opacity

- `transform` and `opacity` can be handled by the compositor without relayout or repaint, so they stay smooth under load.
- Do not animate `width`, `height`, `top`, `left`, `margin`, or `padding` for interface movement. They cause layout on every frame.
- For expanding panels, prefer a transform plus fade, or a grid-row transition (`grid-template-rows: 0fr` to `1fr`), over animating `height`. Verify in the target browsers.
- `box-shadow`, `filter`, and `background` animations cost repaint. Acceptable for small hover effects on a few elements; avoid on lists.
- Avoid animation that shifts surrounding layout (content jumping when something expands). Reserve the space, or animate with transform on an overlay.
- Use `will-change: transform` only on an element that is about to animate, and remove it after. Permanent use wastes memory.

## Never `transition: all`

`transition: all` animates every property that changes, including ones you did not intend (layout properties, colours from theme switches) and ones added later.

```css
/* Before */
.btn { transition: all 200ms; }
/* After */
.btn { transition: background-color 150ms var(--ease-out), transform 120ms var(--ease-out); }
```

Tailwind: use `transition-colors`, `transition-transform`, `transition-opacity`, or `transition-[background-color,transform]`. Do not use `transition-all`. A bare `transition` class in Tailwind covers a preset list of properties, which is still broader than needed; name them.

## Interruptible transitions versus keyframes

- Use CSS transitions for state that the user can change mid-motion (hover, press, toggle, open/close). A transition reverses smoothly from its current value if the state flips.
- Use keyframe animations for one-shot sequences that always run to completion (a loading shimmer, an intro). A keyframe restarts or snaps if retriggered.
- Do not drive a toggle with keyframes: rapid clicks cause jumps.

## Press feedback

Pressed controls respond immediately, with a small scale.

```css
.btn { transition: transform 120ms var(--ease-out); }
.btn:active { transform: scale(0.97); } /* recommended range 0.96-0.98 */
```

- Tailwind: `active:scale-[0.97] transition-transform duration-100`.
- Use only on buttons and tappable cards. Do not scale text inputs, links in running text, or large panels.
- Do not combine press scale with a layout change.
- Disabled elements do not respond to press.

## No animation on high-frequency actions

Things users do many times in a minute should be instant or nearly so: typing, scrolling, keyboard navigation through a list or menu, command palette open, row selection, hover over dense tables. Animation here adds delay, not clarity.

## Stagger for infrequent entrances

For an infrequent entrance of several items (an empty-to-populated list on first load, an onboarding step), a stagger of about 30-60ms per item (recommended) guides the eye. Cap the total (for example the first 8 items) so the last item does not wait. Do not stagger anything users see repeatedly.

```css
.item { animation: enter 300ms var(--ease-out) both; animation-delay: calc(var(--i) * 40ms); }
@keyframes enter { from { opacity: 0; transform: translateY(8px); } }
```

Set `--i` inline from the item index (`style={{ '--i': i }}`). Stagger only where order carries meaning, and keep the whole sequence under about 600ms (recommended).

## Reveal on scroll

- One gentle fade with a small shift (about 12-24px, recommended), using the enter easing and a duration from the table above. Run once per element; it does not replay when the user scrolls back up.
- Trigger with IntersectionObserver, a CSS scroll-timeline, or the animation library the project already uses. Avoid a window scroll listener that reads or writes layout; the cost comes from layout work inside the listener. A passive, throttled listener that does neither is acceptable.
- Pinned, scrubbed or horizontal-scroll sections need a plain fallback that keeps every panel reachable (a normal list, or a scrollable strip with snap points). Check: with reduced motion on, every panel is reachable by keyboard and wheel.
- Undo animation setup on unmount (observers, timelines, listeners). Check: navigate away and back; no duplicate effects.
- At most one auto-scrolling marquee per page, with a pause control (see accessibility-review, 2.2.2).

## Skip animation on first render

Elements that are on screen when the page loads should not animate in unless the entrance is deliberate and infrequent.

- In React, an enter animation on every mounted component replays on every route navigation and on hydration. Gate it: animate on a change after mount, not on mount.
- Do not animate server-rendered content from hidden to visible; it flashes (opacity 0 before hydration) and hurts perceived load.
- Theme switching and initial theme application should not transition colours (set `transition: none` until after first paint, or disable during the switch).

## Reduced motion

Honour `prefers-reduced-motion: reduce`. Replace large movement (translate, scale, parallax, auto-play) with a fade or an instant change; keep functional state feedback such as colour change. State the static end state for each animation (final opacity, final position, no auto-advance); with the setting on, content must be fully visible at rest.

```css
/* Pattern: motion by default, opt out for reduced motion */
.panel { transition: opacity 250ms var(--ease-out), transform 250ms var(--ease-out); transform: translateY(8px); }
.panel[data-open="true"] { transform: none; }

@media (prefers-reduced-motion: reduce) {
  .panel { transform: none; transition: opacity 150ms linear; }
  .btn:active { transform: none; }
  .spinner { animation-duration: 2s; } /* slow, do not remove the progress cue */
}
```

- Tailwind: `motion-safe:transition-transform motion-safe:duration-300` applies motion only when allowed; `motion-reduce:transition-none` removes it.
- Never stop an essential indicator (loading, progress); change its form instead.
- Auto-playing video, looping animation, and carousels must not auto-advance under reduced motion.
- JavaScript animation: read `window.matchMedia('(prefers-reduced-motion: reduce)').matches` and branch. Do the same for scroll-behaviour (`scroll-behavior: smooth` goes inside `@media (prefers-reduced-motion: no-preference)`).
- Check: toggle reduced motion in devtools and confirm no large movement remains.

## Checklist

- Every transition names its properties.
- Durations come from the table or a token.
- Enter uses ease-out, exit uses ease-in and is shorter.
- Only transform and opacity animate for movement.
- No animation on typing, scrolling, or keyboard navigation.
- Reduced-motion branch exists, names its static end state, and was tested.
- Each animation has a written reason; scroll-driven sections have a plain fallback.
