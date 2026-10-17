---
name: ux-review
description: "Reviews Playwright visual-snapshot screenshots (or any screenshot folder) against a UX checklist — layout, spacing, hierarchy, consistency, accessibility, and mobile responsiveness — and reports a rating and findings per screenshot; files GitHub issues only when asked. Use on '/ux-review', 'review these screenshots', 'check the UI on mobile', or 'do a visual UX pass'."
---

# UX Review

## Overview

Read screenshots with the agent's image-reading tool for a UX analysis. Identifies layout issues, spacing inconsistencies, accessibility problems, mobile breakpoint failures, and design system violations.

**Report-first.** The default output is a report. Filing GitHub issues reaches other people, so it happens only when the user asks for it (`--file-issues`, or "file issues for these").

**If the current repo has its own `.claude/skills/ux-review/` or `.agents/skills/ux-review/`, that version is authoritative — follow it instead.** A repo-local version knows the project's design system, breakpoints, and snapshot layout; this one only knows what holds everywhere.

**Announce at start:** "Running UX review."

## Usage

```
/ux-review                     # Review all existing snapshots
/ux-review --fresh             # Run visual tests first, then review
/ux-review --diff              # Review only changed snapshots (git diff)
/ux-review <path>              # Review a specific screenshot or directory
/ux-review --file-issues       # Review, then file GitHub issues for findings
/ux-review --help              # Show this help
```

## Help Flag

When the user passes `--help` (or `help`, `-h`), display this summary and stop:

```
UX Review — AI-Powered Visual Analysis

USAGE:  /ux-review [scope] [options]

SCOPES:
  (default)   Review all existing snapshots
  <path>      Review a specific screenshot file or directory

OPTIONS:
  --fresh     Run visual tests first, then review new screenshots
  --diff      Review only changed snapshots since last commit
  --file-issues
              After the report, file GitHub issues for Needs Attention
              and Needs Fix findings (off by default)
  --help      Show this help

OUTPUTS:
  - Per-screenshot rating (Good/Needs Attention/Needs Fix)
  - Summary with counts
  - GitHub issues for Needs Attention and Needs Fix, only with
    --file-issues or when you ask (issue links then added to the summary)
```

## Dependencies

**axe-core** (optional but recommended for a11y scanning):
```bash
node -e "require('@axe-core/playwright')" 2>/dev/null
```
If missing: suggest `npm install -D @axe-core/playwright` for automated WCAG validation.

## Workflow

### Step 1: Gather Screenshots

**If `--fresh` flag is set:**
Run visual tests to capture current state (project-specific command — check the repo's agent instructions (CLAUDE.md, AGENTS.md) or package.json for the right test command).

**If `--diff` flag is set:**
Only review screenshots that changed since the last commit:
```bash
git diff --name-only HEAD -- '*.png' | grep 'snapshots'
```

**Otherwise:**
Find all snapshot directories:
```bash
find . -path '*-snapshots/*.png' -not -path './node_modules/*' | head -50
```

**If a specific path is given:** Review only that file or directory.

### Step 2: Read and Analyze Screenshots

For each screenshot, use the Read tool to view the image, then evaluate against this checklist:

#### Layout & Spacing
- [ ] Content is properly centered/aligned
- [ ] Consistent spacing between sections
- [ ] No overlapping elements
- [ ] Cards/panels are evenly sized

#### Visual Hierarchy
- [ ] Primary action is prominent
- [ ] Section headers are distinguishable from body text
- [ ] Important information is above the fold

#### Consistency
- [ ] Colors match the project's design system
- [ ] Typography is consistent
- [ ] Button and card styles are consistent across views

#### Mobile Responsiveness (for screenshots with "mobile" in the file name, such as settings-mobile.png)
- [ ] No horizontal scroll
- [ ] Touch targets are at least 44px (Apple Human Interface Guidelines recommend 44x44pt; WCAG 2.2 SC 2.5.8 sets a 24x24 CSS px AA minimum)
- [ ] Text is readable without zooming
- [ ] Forms stack properly on narrow viewports

#### Accessibility (a11y)
- [ ] Sufficient color contrast (WCAG AA: 4.5:1 text, 3:1 large text — WCAG 2.2 SC 1.4.3)
- [ ] Focus indicators visible on interactive elements
- [ ] Form inputs have visible labels (not just placeholders)
- [ ] Error states use color AND text (not color alone)
- [ ] Touch targets at least 44x44px on mobile
- [ ] Heading hierarchy is logical (no skipping levels)
- [ ] Interactive elements distinguishable from static text

**Automated a11y scanning**: If `@axe-core/playwright` is installed, run axe on key pages and report critical/serious violations as 🔴 Needs Fix.

A screenshot cannot prove contrast ratios, focus order, or label associations — treat visual judgments on those as likely findings and say when axe or a manual check is needed to confirm them.

Sources: [WCAG 2.2](https://www.w3.org/TR/WCAG22/) (SC 1.4.1 use of color, 1.4.3 contrast, 2.4.7 focus visible, 2.5.8 target size, 3.3.2 labels or instructions), [Apple Human Interface Guidelines — Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) (44x44pt hit targets), and [axe-core](https://github.com/dequelabs/axe-core) for the automated scan.

### Step 3: Generate Report

For each screenshot reviewed:

```
## UX Review Report

### [screenshot-name.png]
**Rating:** 🟢 Good / 🟡 Needs Attention / 🔴 Needs Fix

**Issues:**
- [severity] [description] — [suggestion]

**Positives:**
- [what works well]
```

Severity levels:
- **Critical**: Broken layout, unusable on mobile, accessibility violation
- **Major**: Inconsistent spacing, unclear hierarchy, poor mobile UX
- **Minor**: Slight misalignment, could-be-better contrast, polish items

### Step 4: Ask, Then File Issues (only on request)

**Default: do not file anything.** End the report by listing the 🟡 Needs Attention and 🔴 Needs Fix findings and asking whether to file GitHub issues for them. File issues only when the user passed `--file-issues` or says to file them (all, or the ones they name).

When filing:

1. Detect the repo's issue conventions instead of assuming them:
   - Issue templates: `ls .github/ISSUE_TEMPLATE/ 2>/dev/null` — if a bug or enhancement template exists, follow its sections.
   - Labels: `gh label list --limit 200` — use an existing label that fits (for example a bug-type label for 🔴 and an enhancement- or UX-type label for 🟡). **Never create labels.** If nothing fits, file without a label and say so.
   - Title style: `gh issue list --limit 20 --state all` — match the repo's prevailing title format (for example a conventional `fix(ux): ...` prefix only if the repo uses one).
   - The repo's agent instructions (CLAUDE.md, AGENTS.md) or CONTRIBUTING.md, if they say how issues should be written.

2. Create each issue with:
   - A title in the repo's style describing the problem
   - The detected label, if one fits
   - Body: screenshot path, rating, all issues found, and positives (inside the template's sections when there is a template)
   - Group related findings into a single issue when they share the same root cause

3. Report each issue URL in the review output

**Do NOT file issues for:**
- 🟢 Good rated screenshots
- Known, already-tracked issues (check existing GitHub issues first: `gh issue list --search "<keywords>" --state all`)
- Platform-specific rendering differences

### Step 5: Summary

```
UX Review Complete:
- Screenshots reviewed: N
- 🟢 Good: N
- 🟡 Needs Attention: N
- 🔴 Needs Fix: N
- Issues filed: N (links) — or "not filed; reply 'file issues' to file them"
```

## Worked example

User: `/ux-review tests/visual/__snapshots__/checkout-mobile.png`

1. Read the screenshot. It shows a mobile checkout form at 390px wide.
2. Findings: the "Place order" button is a low-contrast grey on white, the email field uses placeholder text instead of a label, and the promo-code row overflows to the right, causing horizontal scroll.
3. Report:

```
### checkout-mobile.png
**Rating:** 🔴 Needs Fix

**Issues:**
- [Critical] Promo-code row overflows the viewport, causing horizontal scroll — let the input shrink or stack the button below it
- [Major] Email field has a placeholder but no visible label — add a persistent label above the field
- [Major] "Place order" button text looks below 4.5:1 contrast — confirm with axe; darken the button color if it fails

**Positives:**
- Single-column layout and a clear order summary at the top
```

4. Summary: 1 reviewed, 1 🔴 Needs Fix, issues filed: 0. "Want me to file a GitHub issue for the checkout findings?" Nothing is filed until the user says yes.
