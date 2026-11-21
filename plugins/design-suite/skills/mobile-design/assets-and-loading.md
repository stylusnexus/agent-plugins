# Assets and loading

Complements `performance-and-offline.md` (srcset basics, lazy-load, layout shift, offline states). This file adds image encoding decisions, budgets, first-paint control and failure testing. Thresholds are recommended defaults; device mix and network are MISSING INFORMATION unless supplied. Report-only: list findings, do not change build tooling unasked.

## 1. Served pixels

- Compare three counts: CSS box, file pixels, physical screen pixels (CSS box times density). Check: natural width is at most CSS width times 2 (recommended ceiling; 3x phones are an exception to justify). Flag any file wider than that.
- Oversized files cost decode time and memory on low-end phones, not only bytes. Check: profile a low-end device and look for jank or blank tiles while scrolling image-heavy screens.
- Every image has width and height or an aspect ratio. Check: layout-shift audit lists no image or embed without dimensions.

## 2. Format decision

| Question | Check |
|---|---|
| Photo or illustration? | Photo: lossy raster. Illustration with flat colour: vector or palette PNG |
| Needs transparency or animation? | Transparency rules out plain JPEG |
| Logo or icon? | Vector (SVG), not a raster |
| Does the audience's browser open it? | Provide a fallback chain; confirm support before rollout |

- No SVG contains an embedded raster; one hidden bitmap can multiply file size. Check: open each SVG source for image elements.
- Animated GIF becomes muted, looping, inline video with a poster frame. Check: `autoplay muted loop playsinline` plus a `poster` are present; reduced motion is honoured, and a pause control exists if it runs over 5 s (2.2.2).

## 3. Quality and re-encoding

- Assign each image a quality tier (best, good, low, lowest) by prominence and bandwidth importance. Check: every asset class has a written tier.
- Judge quality with a perceptual metric (for example SSIM or Butteraugli) against a recorded target, never the encoder slider; slider numbers do not transfer between tools or formats. Check: the target score is recorded per asset class.
- Never re-encode an already lossy file; each pass stacks artefacts. Keep lossless masters. Check: the build input is the original master, not a re-encoded derivative.
- Keep full colour detail (no chroma subsampling) for text-heavy images, diagrams, logos and UI screenshots. Check: zoom on coloured text and hard edges for fringing.
- Few-colour UI art goes to a palette PNG, not 32-bit. Check: flag PNGs with 256 or fewer colours and no soft alpha.
- sRGB is the default; wide gamut only where saturated colour matters. Check: embedded colour profiles are justified (they can be heavy).
- Text over a photo: judge contrast at the lightest region the text covers, not the average. Use a gradient scrim or solid overlay, or move the text to a solid panel. Check: for every text-on-image, name the worst-case region and the ratio (4.5:1 body, 3:1 large); test with the lightest crop and with the image failed or loading.
- Automatic compression can shift brand colours and skin tones. Check: compare brand and people images with source before rollout.

## 4. Byte budget

- Set a byte budget for images per page, per device class (mobile and desktop budgets differ). Number: owner decision, no default supplied. Check: measure total image bytes for each key page and compare; a breach goes to the owners as a trade-off.
- Each image earns its place; fewer decorative images can help conversion. Check: list decorative images and justify or remove each.
- Lazy-load below the fold, never the hero or first screen. Hidden-by-CSS images still download. Check: no lazy attribute above the first viewport; no requests for CSS-hidden variants.
- Placeholder then fade in: the preview resembles the final image and is small (recommended about 1 to 2 KB). Check: first paint shows a recognisable preview; no pop-in.
- Cache: hashed URLs cache long; format-negotiated images send a Vary header. Check: each image response has a deliberate cache policy.

## 5. Fonts and the first-paint set

- Choose a font-display behaviour (swap or optional) so text is never invisible for more than a moment; subset fonts to needed scripts. Check: throttle the network and look for blank text.
- Name the first-paint set: the styles, scripts, fonts and image that the first screen needs. Check: write the list; anything else is deferred.
- Only styles for the first screen are render-blocking. Check: no head stylesheet that styles only below-the-fold content.
- Core content readable with scripts off or failed. Check: disable scripts and confirm text and primary links appear.
- Preload hints set `as` (and `crossorigin` for fonts), or the file downloads twice. Check: no duplicate requests in the network panel.

## 6. Failure tests

- Block each third-party script in turn; the page must still render. Check: if it does not, defer it or isolate it in a frame.
- Define a failure state per resource type when offline or failing: image (alt text, layout holds), font (fallback), script (core content), video (poster), data (message with retry). Check: force a 404 on each image slot and confirm layout and alt text.
- Save-Data: when the data-saver signal is on, serve smaller variants, load one carousel item at a time, skip autoplay and decorative media. Check: run with the signal on; each media component has a defined lighter state.
- Test on the weakest target device and throttled network; the page shows something useful within a few seconds (recommended; confirm threshold). Checks not performed (real device, throttled run) must be listed.
