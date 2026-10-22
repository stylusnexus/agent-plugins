# Testing methods and honest reporting

## What a source-only review can and cannot show

Can show (VERIFIED from code): missing labels or alt, click handlers on non-interactive elements, `outline: none` without replacement, `tabindex` > 0, invalid or redundant ARIA, missing `lang`, heading skips in the markup, hard-coded token pairs and their computed contrast, fixed widths, `maximum-scale`, missing `prefers-reduced-motion` handling, absent `autocomplete`.
Cannot show (NEEDS-TEST): the computed accessibility tree, final rendered colors and stacking, real tab order and visual order, focus behavior after state changes, whether a live region is announced, how a screen reader reads a widget, what third-party components render, runtime-injected content, behavior at other zoom levels and viewports, sticky elements obscuring focus, text over user images, whether copy is understandable to a person.
Say at the top of the report which of the two applies.

## Manual keyboard pass (browser required)

Use only the keyboard. Unplug the mouse mentally: no clicking.
1. Reload the page. Press Tab once. Expect a skip link or the first meaningful control, visibly focused.
2. Tab through the whole page. At each stop, check: focus indicator visible; order matches visual order; element name/purpose clear; no stop on a non-interactive item; nothing hidden under a sticky header or banner.
3. Shift+Tab backward across the same path; confirm same stops, no traps.
4. Activate every control: Enter on links and buttons, Space on buttons, checkboxes, and switches; arrows in radio groups, tabs, menus, selects, sliders; Esc to close popovers and dialogs.
5. Open each dialog, menu, and popover: focus moves in; Tab stays in modal; Esc closes; focus returns to the trigger.
6. Submit each form empty and with bad data: focus goes to the error summary or first error; messages are text.
7. Trigger route changes, delete/add rows, and async loads: note where focus lands.
8. Try every pointer-only function (hover, drag, right-click, long-press, swipe) and confirm a keyboard equivalent.
9. Note any key that does nothing, any keyboard trap, and any hidden-yet-focusable content.
Record each stop as: step, element, observed focus, issue.

## Zoom and reflow pass (browser required)

1. At 100 percent, note the layout. Zoom to 200 percent: no clipped text, no overlapped controls, nothing lost (1.4.4).
2. Set width to 320 CSS px (DevTools device toolbar, or zoom to 400 percent on a 1280 px window). Check no horizontal scroll except in tables, maps, and similar (1.4.10) and all tasks still work.
3. Inject text spacing: line-height 1.5, paragraph spacing 2em, letter-spacing 0.12em, word-spacing 0.16em, via DevTools or a user style; confirm no clipped or overlapping text (1.4.12).
4. Toggle emulated rendering: `prefers-reduced-motion: reduce`, `prefers-reduced-transparency: reduce` (where supported), dark `prefers-color-scheme`, `forced-colors: active`, and vision-deficiency simulation (grayscale/achromatopsia) to check color-only meaning.
5. Rotate/resize to landscape and portrait (1.3.4).
6. Repeat keyboard focus checks at 320 px with sticky elements visible.

## Screen-reader pass: VoiceOver on macOS (human/at-tool required)

Needs a person at the machine or a tool that drives VoiceOver. An AI cannot hear speech output from source alone; if not run, list as not performed.
- Start/stop: Cmd+F5 (not confirmed from Apple's guide pages; check the VoiceOver User Guide). VO modifier is Control+Option.
- Safari is the most reliable VoiceOver pairing; Chrome works but differs. Record the browser and macOS version.
- Rotor (VO+U, confirmed in Apple's VoiceOver User Guide): open Headings, Links, Landmarks, Form Controls; confirm each list is complete, ordered, and has meaningful names.
- Read by item: VO+Right/Left. Interact with groups: VO+Shift+Down; leave: VO+Shift+Up (these two not confirmed from Apple's guide pages; check them).
- Check: page title announced on load; landmarks present; headings outline; every control announces name, role, and state (expanded, selected, checked, invalid, required); form hints and errors are read with the field; dialogs announce their name and trap reading; live regions speak after an action; images read alt or are skipped; tables announce headers.
- Sequence to run: load page, rotor headings, rotor landmarks, move through the main task, trigger an error, trigger a status message, open and close a dialog.
- Tab-key focus and VoiceOver cursor navigation are different paths; test both, since a control can be reachable by one and not the other.
- Not tested here: NVDA, JAWS (Windows), TalkBack (Android), VoiceOver on iOS, Narrator, Dragon voice control. Say so in the report. ARIA behavior varies across them.

## Automated checks with axe

Use what is already installed. Do not install anything; if axe is absent, list "automated scan: not run, axe unavailable" under checks not performed.
- Browser extension: axe DevTools or Lighthouse accessibility audit in Chrome; run on each state (dialog open, error shown, dark mode).
- Playwright with `@axe-core/playwright` if the repo already has it:
```ts
import AxeBuilder from "@axe-core/playwright";
const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
  .analyze();
expect(results.violations).toEqual([]);
```
- Scan more than the initial load: open menus and dialogs first, trigger validation, switch themes, resize.
- Automated tools detect only a portion of issues (commonly cited as roughly a third to a half; do not quote a number as fact). They cannot judge whether alt text is meaningful, whether focus order is logical, whether labels make sense, whether a keyboard trap exists in practice, or whether a screen reader reads correctly. They report "incomplete" items needing manual review; list those.
- A clean scan means "no violations found by this tool on these states".
- Contrast: measure, do not eyeball.
- Core Web Vitals (published "good" levels: LCP 2.5 s, INP 200 ms, CLS 0.1) come from a real browser or field data. Lighthouse lab runs do not measure INP.

## Findings log template

```
ID: A11Y-001
Priority: Blocker | Serious | Moderate | Minor
WCAG: 2.4.7 Focus Visible (AA)         # or "criterion not confirmed"
Location: components/Nav.tsx:42  |  /pricing  |  nav a.cta
Observed barrier: <quote markup/style or describe behavior>
Affected interaction: keyboard users tabbing through primary navigation
Priority rationale: <who is blocked, which task, how often>
Fix: <code or exact change>
Evidence: VERIFIED (source) | VERIFIED (browser, Chrome, 200%) | NEEDS-TEST (VoiceOver)
Status: open | fixed (retest needed)
```

## Honest wording

Use:
- "No violations were found in the checks run: <list>. Not run: <list>."
- "Review of source only; rendered behavior and assistive-technology output were not tested."
- "These findings are candidates for a full accessibility audit by qualified testers."
- "Likely failure of 1.4.3 pending contrast measurement in the rendered page."

Do not use: "conforms to WCAG 2.2 AA", "is accessible", "is compliant", "passes accessibility", "certified", "ADA/EAA/Section 508 compliant", or "meets requirements" about the whole interface. A pass on individual checks is reported per check ("keyboard pass on /settings: no traps found in the steps run").
Passing automated scans does not demonstrate conformance. Conformance claims also require the full scope of pages and states, all applicable criteria, and human testing with assistive technology, and legal conclusions belong to qualified professionals.
