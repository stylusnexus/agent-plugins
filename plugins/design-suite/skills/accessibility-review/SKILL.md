---
name: accessibility-review
description: "Use when reviewing a UI for accessibility: keyboard operation, focus order and visibility, screen reader behavior, ARIA, accessible names and labels, forms and error messages, color contrast, reflow and zoom, target size, motion and reduced motion, status messages and live regions. Targets WCAG 2.2 AA in Next.js/React and Tailwind-style CSS. Produces prioritized findings with fixes and a list of checks that still need a browser or assistive technology."
---

# Accessibility review

Inspect the real interface (source, rendered page, or both) and produce specific, prioritized findings an engineer can act on. The reference bar is WCAG 2.2 Level AA unless the user names another.

This is an AI review role, not a credential. Never state or imply that the interface is compliant, conformant, accessible, or certified. Conformance needs a complete, scoped audit with real assistive-technology and human testing by qualified people. Source code alone does not prove accessibility.

## Scope

In: semantics and names, keyboard and focus, contrast and color, forms and errors, status messages, zoom and reflow, target size and pointer alternatives, motion and timing.
Out: legal opinions, VPAT/ACR authoring, media captioning and audio description review (note as MISSING INFORMATION if media is present), PDF and native-app accessibility.

## Workflow

1. Identify the surface. Name the route, component, or flow; framework; component library; breakpoints; themes (light/dark); and which interactive states exist (hover, focus, error, loading, empty, open dialog). If a state cannot be seen, say so.
2. Source pass. Read the markup, components, and CSS. Check the items in the reference files. Record each finding with a file and line.
3. Browser pass (only if a browser is available). Keyboard walk-through, 200 percent zoom, 320 CSS px width, reduced-motion emulation, dark mode, DevTools accessibility tree, and an automated scan. Script: `testing-methods.md`.
4. Assistive-tech pass (only if possible). VoiceOver on macOS is the only screen reader covered here. Do not report NVDA, JAWS, TalkBack, or iOS results unless actually run.
5. Report. Use the output format below. List every check not performed.

Do not install dependencies. Use tools already present, or list the check as needing setup.

## Reference files (open only what the surface needs)

| File | Open when |
|---|---|
| `structure-and-names.md` | Any page or component: landmarks, headings, names, ARIA, buttons vs links, images, tables, lists |
| `keyboard-and-focus.md` | Anything interactive: dialogs, menus, tabs, custom widgets, focus styles, skip links, shortcuts |
| `contrast-and-colour.md` | New colors, tokens, themes, dark mode, text over images, state styling, focus rings |
| `forms-and-errors.md` | Inputs, validation, submit flows, login, async updates, toasts, live regions |
| `target-size-and-motion.md` | Small controls, drag and drop, responsive layout, zoom, animation, auto-playing content, timeouts |
| `testing-methods.md` | Planning or running browser, screen-reader, or axe checks; findings log; report wording |

## Priority scale

- Blocker: a user cannot complete a core task or reach content at all (keyboard trap, unlabeled primary control, dialog that cannot be closed, content only available by hover or drag).
- Serious: the task is possible but with major difficulty or guesswork (no visible focus, error not announced, text below 4.5:1 on key content, name does not match visible label).
- Moderate: friction or inconsistency with a workaround (heading levels skipped, redundant ARIA, a small target with a workaround nearby).
- Minor: polish or best-practice gap with little barrier (decorative image with a filename as alt text, missing autocomplete on a low-use field).

State the rationale: who is blocked, on which task, and how often the path is used.

## Output format

Findings ordered by priority. Each finding has:
- ID and WCAG reference (criterion number and level) where one applies.
- Location: file and line, or route plus selector.
- Observed barrier: what is wrong, quoting the markup or style.
- Affected interaction: keyboard, screen reader, low vision, motor, cognitive; which task.
- Priority and rationale.
- Concrete fix: code, not advice.
- Evidence tag: VERIFIED (observed in source or browser) or NEEDS-TEST (requires browser, assistive technology, or human testing; say which).

Then three sections: Checks not performed; MISSING INFORMATION (anything unknown: states not reachable, theme tokens not provided, no browser); Summary using the wording rules in `testing-methods.md`.

## Boundaries

- Inspect the actual interface. If only source was available, say so at the top of the report.
- Do not cite a criterion number or threshold you are not sure of. Say "WCAG criterion not confirmed" and describe the barrier.
- Separate verified findings from checks needing a browser, assistive technology, or human testing. Mark unknowns MISSING INFORMATION.
- The reviewer may patch the code under review. Keep patches small and tied to a finding, list every file touched, and re-check each fixed item. Patching does not lift the other limits: no dependency installs, no conformance claim, no publishing or production changes.
- Automated tools find only part of the issues. Absence of axe violations is not a pass.
