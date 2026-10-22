# Performance, offline and motion on mobile

Treat connection and CPU as unknown until measured. Do not claim audience network conditions; mark MISSING INFORMATION. The thresholds below named "Core Web Vitals" are Google's published "good" levels at the 75th percentile; other numbers are recommended defaults.

## 1. Slow network and offline states

Design these explicitly (the ui-ux skill holds the full state list):
- Slow: show skeletons or the stable shape of the final layout; keep headline content and primary action usable before secondary content loads; show progress for operations beyond about 1 s (recommended).
- Offline: detect connectivity loss (`navigator.onLine` is a hint, not proof; confirm with failed requests), show a persistent, non-modal indicator, and say what still works.
- Reading: keep already-loaded content visible and usable offline. Mark it with its age.
- Writing: either queue changes visibly ("Will send when you are back online", with count and ability to cancel) or disable the action with a reason. Never imply a queued change is saved on the server.
- Conflicts: if the same item changed elsewhere, say so and let the user choose; do not silently overwrite.
- Retry: manual retry button plus automatic retry with back-off; tell the user which is happening. Do not auto-retry non-idempotent actions.
- Interrupted tasks: preserve drafts and form state across reload, tab discard and returning later; offer "continue where you left off".
- Failure mid-upload or checkout: say whether anything was charged or sent, and how to confirm.
- Caching and offline storage have privacy implications for sensitive data; get a decision from the product owners before storing personal data on device.
- Whether to build an offline-capable app (service worker, local store) is a product and effort decision for the product owners; present options and costs, do not add libraries.

## 2. Images and media

- Serve images at the size they are displayed: provide `srcset` and `sizes` so small screens download small files; specify real `width` and `height` (or `aspect-ratio`) to reserve space.
- Use modern formats the stack already supports (AVIF/WebP with fallback) without adding build tools unasked.
- Lazy-load below-the-fold images with `loading="lazy"`; do not lazy-load the largest above-the-fold image; consider `fetchpriority="high"` for it.
- Avoid autoplay video on mobile; if used, muted, short, with controls and respect for data-saver and reduced motion preferences.
- Provide text alternatives; decorative images get empty `alt`.
- Prefer CSS or SVG for simple graphics.
- Avoid shipping desktop-sized assets "scaled down by CSS".

## 3. Tap latency and responsiveness

- Give feedback at once: pressed state within the first frame or two (well under 100 ms; Core Web Vitals "good" Interaction to Next Paint is 200 ms or less).
- Use `touch-action: manipulation` to remove the double-tap-zoom delay on controls in browsers that still apply one. With `width=device-width` most modern mobile browsers already avoid the delay; verify.
- Keep main-thread work short: split long tasks, defer non-critical scripts, avoid heavy synchronous handlers on tap.
- Do not require double taps; do not rely on hover.
- Optimistic UI is acceptable only if failure is shown and reverted visibly.

## 4. Avoiding layout shift

Core Web Vitals "good" Cumulative Layout Shift is 0.1 or less.
- Reserve space for images, embeds, ads, banners and late-loading components.
- Skeletons match final dimensions.
- Insert new content above the viewport only on user action; do not push content the user is reading or about to tap.
- Web fonts: use `font-display` and size-matched fallback fonts to limit text jumping.
- Keep the toolbar, sticky headers and bottom bars at constant heights; animate with `transform` rather than layout properties.
- Cookie and consent banners overlay or reserve space rather than shoving content down after load.
- Largest Contentful Paint "good" is 2.5 s or less on the same basis; treat as a target to measure, not an assumption about this product.

## 5. Battery-friendly motion

- Animate `transform` and `opacity`; avoid animating layout properties (`width`, `top`, `margin`).
- Keep animations short and purposeful (recommended: roughly 150 to 300 ms for UI transitions) and use easing that settles.
- Avoid continuous background animation, large blurs and heavy shadows on scrolling content; they drain battery and drop frames.
- Pause animations and video when off-screen or the tab is hidden.
- Avoid polling loops; prefer pushes or longer intervals, and stop updates in the background.
- Limit location, sensor and camera use to when needed and release afterwards.

## 6. Reduced motion

- Respect `prefers-reduced-motion: reduce`: replace large movement (parallax, zooming, sliding panels, auto-scrolling) with fades or instant changes; remove auto-playing animation.
- Do not remove motion that carries information; provide an equivalent (text, state change).
- Provide a way to pause, stop or hide anything that moves automatically for more than 5 seconds (WCAG 2.2.2, level A).
- Avoid flashing more than three times in one second (WCAG 2.3.1).
- Motion triggered by interaction should be disable-able (WCAG 2.3.3 at level AAA; good practice).
- Test with the system setting on.

## 7. Acceptance checks

- Throttle the network in browser dev tools to a slow profile and walk the main task; note what is blocked.
- Switch to offline mid-task; confirm indicator, preserved input and honest messaging.
- Run a layout-shift check on key pages; list shifts and the element causing each.
- Image sizes in the network panel are proportionate to display size.
- With reduced motion on, no large movement remains.
