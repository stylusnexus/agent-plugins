# Target size, reflow, and motion

Related criteria: 1.3.4, 1.4.4, 1.4.10, 1.4.12, 2.2.1, 2.2.2, 2.3.1, 2.3.3, 2.5.5, 2.5.7 (new in 2.2), 2.5.8 (new in 2.2).

## Target size

### Minimum (2.5.8, AA, new in 2.2)

Pointer targets are at least 24 by 24 CSS px, with these exceptions:
- Spacing: an undersized target passes if a 24 CSS px diameter circle centered on its bounding box does not intersect another target or another undersized target's circle. Small icon buttons with at least enough gap pass.
- Equivalent: the same function is available through another conforming control on the same page.
- Inline: the target sits within a sentence or its size is constrained by surrounding text (links in a paragraph).
- User agent control: size is set by the browser (native checkbox/range unmodified).
- Essential: the presentation is required (for example a map pin).

### Enhanced (2.5.5, AAA)

At least 44 by 44 CSS px, with similar exceptions (equivalent, inline, user agent, essential). Not required at AA.

### Platform guidance is a different bar

Apple suggests a 44 by 44 pt minimum and Material Design 48 by 48 dp. These are design recommendations for touch, not WCAG conformance levels. Use them for touch-first products as recommended practice, and report a miss against them as Minor/Moderate recommendation, not as a WCAG failure. 44 CSS px covers 2.5.5 and approximates Apple's guidance.

### Checking and fixing

- Measure rendered size in DevTools (the box that receives the click, including padding), not the icon's size. The hit area can exceed the visible glyph with padding.
- Tailwind: `size-6` is 24px, `h-6 w-6` is 24px, `p-2` around a 16px icon makes 32px. `min-h-11 min-w-11` is 44px (11 x 4px).
- Extend hit areas without shifting layout:
```css
.icon-btn { position: relative; }
.icon-btn::after { content: ""; position: absolute; inset: -8px; } /* enlarges hit area; must not overlap neighbours */
```
- Overlapping hit areas, adjacent destructive and safe actions with no gap, and dense table row actions are the usual failures.
- Check at 320 px width and 200 percent zoom, where controls crowd.

## Pointer alternatives

- Dragging (2.5.7, AA, new in 2.2): any action done by dragging (sortable lists, sliders implemented as custom drag, kanban, file reorder, drag-to-resize) needs a single-pointer alternative: click-to-select then click-to-place, up/down buttons, or a menu "Move to...". Keyboard support alone does not satisfy 2.5.7, but add it too (2.1.1). Exception: dragging is essential. Native `<input type="range">` is a pass.
- Pointer gestures (2.5.1, A): multi-point or path gestures (pinch, two-finger swipe, drawn path) need a single-pointer alternative such as zoom buttons.
- Pointer cancellation (2.5.2, A): trigger actions on `click`/`pointerup`, not `pointerdown`/`mousedown`, so the user can move away to abort; if down-event is used, provide abort or undo.

## Reflow, zoom, and text spacing

- Reflow (1.4.10, AA): content must work at a viewport 320 CSS px wide (equivalent to 400 percent zoom on a 1280 px window) with no two-dimensional scrolling and no loss of content or function. Content needing two-dimensional layout is exempt: data tables, maps, images, video, games, and toolbars may scroll in both directions. Horizontal scroll is acceptable only for those. For content that scrolls horizontally, the equivalent test is a 256 CSS px viewport height.
  - Common failures: fixed widths (`w-[600px]`), `min-w-*` on containers, `whitespace-nowrap` long labels, `overflow-x` hidden clipping content, fixed-position panels taller than the viewport, sidebars that do not collapse, `100vh` panels with hidden overflow.
  - Check: set the browser window or DevTools device width to 320, zoom to 400 percent, and walk every task.
- Resize text (1.4.4, AA): text can scale to 200 percent without loss of content or function (browser zoom or text-only zoom). Failures: font sizes in `px` with fixed-height containers that clip, `overflow: hidden` with fixed `height`, `line-clamp` hiding essential content, `user-scalable=no` or `maximum-scale=1` in the viewport meta (blocks pinch zoom on mobile; remove).
  - Prefer `rem` for font sizes and `min-height` over `height`.
- Text spacing (1.4.12, AA): no loss of content or function when a user sets line-height 1.5 times the font size, paragraph spacing 2 times the font size, letter-spacing 0.12 times the font size, word-spacing 0.16 times the font size. Test with a user stylesheet or bookmarklet; failures are clipped text in fixed-height buttons, tabs, cards, and truncation that hides content.
- Orientation (1.3.4, AA): do not lock to portrait or landscape (`screen.orientation.lock`, CSS rotate transforms that force one orientation) unless essential (for example a piano app).
- Sticky headers and cookie banners that eat a large share of a short viewport at 400 percent zoom are a recurring reflow and focus-obscured problem (see 2.4.11 in `keyboard-and-focus.md`).

## Motion

### Reduced motion

`prefers-reduced-motion: reduce` is the OS setting. Honor it for non-essential motion: parallax, large translate/scale, auto-scrolling, spinning, bouncing. Reduce rather than only remove: swap movement for a fade or instant change when the animation carries meaning.
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
Tailwind: `motion-safe:animate-bounce` (only when no preference) or `motion-reduce:transition-none`. Prefer `motion-safe:` for decorative motion, so default is still.
JS-driven animation (Framer Motion, GSAP, scroll listeners) ignores the CSS query: check `window.matchMedia("(prefers-reduced-motion: reduce)").matches` or the library's reduced-motion hook. Videos that autoplay should not when this is set.

State the static end state for each non-trivial animation (final opacity, final position, no auto-advance). With the setting on, content is fully visible at rest.

The preference is guidance; the WCAG criteria below are the pass/fail rules. The media query alone does not satisfy 2.2.2: auto-moving content longer than 5 seconds (marquees, carousels, looping micro-animations) also needs a pause, stop or hide control for users who have not set the preference.

Scroll-pinned and horizontal-scroll sections need a keyboard-reachable, non-animated alternative that reaches every panel. A scrollable region must be focusable (`tabindex="0"` with a name). Custom cursors are a polish flag (Minor): check they do not hide the pointer or shrink it below a usable size and contrast.

### Criteria

- Pause, stop, hide (2.2.2, A): moving, blinking, or scrolling content that starts automatically, lasts more than 5 seconds, and is presented in parallel with other content needs a mechanism to pause, stop, or hide it. Carousels and auto-advancing banners, background video, animated GIFs, and marquees are typical. Auto-updating content (tickers, live feeds) needs pause/stop/hide or a user control for the update frequency, unless essential. Controls must be keyboard-reachable and early in the DOM order near the content.
- Three flashes (2.3.1, A): no content flashes more than three times in any one-second period, unless below the general flash and red flash thresholds. If any flashing exists, flag Serious pending measurement; do not attempt to certify safety. Spinners and fades are normally not flashing.
- Animation from interactions (2.3.3, AAA): motion animation triggered by interaction can be disabled unless essential. Not required at AA but `prefers-reduced-motion` handling usually meets it.
- Auto-play audio longer than 3 seconds needs a control to pause or mute independent of system volume (1.4.2, A).

### Timeouts (2.2.1, A)

If a session or form has a time limit, the user can turn it off, adjust it to at least 10 times the default, or extend it with a simple action (for example "Press any key to extend") after a warning of at least 20 seconds, with at least 10 chances to extend. Exceptions: real-time events, essential limits, and limits longer than 20 hours. Check session-expiry modals, auto-logout, checkout holds, auto-dismissing toasts that contain required information or controls, and OTP validity (give a way to resend). Toasts with actions should persist until dismissed or be long enough to read and act; there is no fixed WCAG number for toast duration, so report brevity as a risk under 2.2.1 only if the toast is a time limit on the user's task.
