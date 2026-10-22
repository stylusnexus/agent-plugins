# Findability review (if the user can't find it, it isn't there)

A findability review checks whether users can reach and recognise a feature, and whether a change buried or moved something. It is an expert review from the diff and the screens, not user research. Say so in the output. Findings are hypotheses; list which need a browser, assistive technology, or real people.

## How to run it

1. Fix the scope: which feature or screens the change touches, which user, which devices.
2. Read the diff and the code, not only screenshots.
3. For each feature or screen, run the six checks below and cite evidence for each.
4. Log findings with severity, evidence, the findability result and a recommendation.

## The six checks

1. Entry points. Where does the user reach this from, and in how many steps? Navigation, menus, flyouts, popovers, empty states, search or command palette, and the mobile equivalent. Look for: route lists, nav and menu config, links into the page. Evidence: file:line of each entry, or the click path. Example: "Export is only reachable from the row menu at src/Table.tsx:88; the toolbar entry was removed, so it is now three steps."
2. Naming. Does the label say what the user would call it, and is it the same word everywhere? Look for: renamed or new labels, internal terms in UI strings, one feature called two things. Evidence: the strings and where they appear. Example: "The page is titled Workspaces but the menu item says Projects (nav.ts:14, Header.tsx:41)."
3. Visibility. Is it visible by default, or behind hover, a flyout, a disclosure or a breakpoint? If behind something, is the way in signposted, and reachable by keyboard and touch? Look for: hover-only reveals, feature flags, `display: none` or `hidden` under a breakpoint, icon-only controls, disclosure defaults. Evidence: the rule or flag and the condition. Example: "The filter bar is hidden below 768px (filters.css:30) with no replacement control, so phone users cannot filter."
4. Placement. Does a popover, flyout or menu open where the user is looking, stay inside the viewport, and avoid covering what it relates to? Look for: popover or menu anchoring and offset, fixed widths, positioning with no collision handling, overlays over their own trigger. Evidence: the positioning code and, if available, a screenshot at a narrow width. Example: "The flyout opens to the right of a right-aligned button and is clipped at the viewport edge (Flyout.tsx:52, no flip)."
5. Progressive disclosure. Is the first view the right amount, and is more one clear step away? Look for: primary tasks pushed behind "More", everything shown at once, collapsed sections with no hint of contents. Evidence: the default state in code or screenshot. Example: "The only way to change the plan is a link inside the collapsed Advanced section (Settings.tsx:120)."
6. Regression. Compare before and after. Look in the diff for removed or renamed routes, nav and menu config, labels, feature flags, and responsive rules that hide things. Evidence: the removed and added hunks. Example: "The /reports route was removed (routes.ts:22) and no redirect or menu entry replaces it."

## Before and after without a baseline

Where the repo keeps no baseline screenshots, compare from the code:

1. Read the base branch's nav config, route list and labels (`git show <base>:<path>` or the diff context).
2. Compare them with the changed versions: what moved, was renamed, was removed, or is now conditional.
3. State plainly in the output that the visual comparison was not made, and list it under not verified.

Run the app only if the caller gave the command.

## Severity

- Blocker: the user cannot reach the feature or finish the task.
- Major: reachable only by hover, by guessing, or at one breakpoint, input method or role.
- Minor: label or placement friction; the user gets there with some extra effort.

Severity is a judgement. Say what it rests on.

## Issue body

One issue per distinct concern. File only defects and regressions with evidence; preferences and second opinions stay in the answer.

```
**What a user cannot find or do:** <one sentence in the user's words>
**Where:** <screen, route, breakpoint, input method>
**Evidence:** <file:line, diff hunk, or screenshot name>
**Suggested fix:** <the smallest change that restores the path>
```

## Duplicate search

Before filing, search open and closed issues in the repository the change belongs to:

1. `gh issue list --state all --search "<terms>"`, using the feature name, the old and new label, and the route.
2. Read the hits. If one covers the concern, do not file a second; comment only with new evidence.
3. Use the repository's own templates and labels. If no label fits, file without one and say which is missing.

## Output

Findings (severity, evidence, findability result, recommendation), a regression section (what moved or got buried, before and after), a not verified list, and links to issues filed or already existing. Close with what was reviewed, what was not, and the user tests that would confirm or overturn the top findings (see heuristics-review.md for the shared output habits).
