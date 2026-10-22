# Review format

Use this template for every report, whether or not code was changed.

## Template

```
## Interface polish: <screen or component>

Read: <one line: what the surface is, who it is for, the feeling it aims for, the design system it sits in>
Assumptions: <list; if intent is unclear, ask one question, not several>
Scope: <files or routes reviewed>
Design system used: <token file / config path, or "none found">
Mode: <report only | implemented>

### Before / After

#### <Design principle, for example "Concentric radius">
| Principle | Before | After | File |
| --- | --- | --- | --- |
| Concentric radius | Card rounded-lg around button rounded-lg, padding 16px | Card rounded-3xl (8px inner + 16px padding) | components/Card.tsx |

#### <Next principle>
| Principle | Before | After | File |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

### Not fixed
| Severity | Principle | Finding | File |
| --- | --- | --- | --- |

### Files touched
- <path> (omit this section in report-only mode)

### Checklist
(see below)

### Could not verify
- <item and why>
```

Rules for the table:

- Group rows under one heading per design principle. Use the principle names from the reference files (spacing, radii, elevation, motion, typography, colour, states, layout, forms).
- Columns are exactly: Principle | Before | After | File.
- Before and After state concrete values or class names, not adjectives ("transition-all" and "transition-colors duration-150", not "bad" and "better").
- In report-only mode, After describes the recommended change and the File column names where it applies.
- One row per change. Do not merge unrelated changes.
- File uses a path from the repository root and, when useful, a line number.

## Severity scale

| Level | Meaning | Examples |
| --- | --- | --- |
| Blocker | Breaks use or fails a standard; fix before merge | no visible keyboard focus, text clipped at 320px, content unreadable in dark mode |
| Major | Clearly wrong and noticeable; fix soon | `transition: all`, missing disabled or error state, layout shift on hover |
| Minor | Inconsistent or unrefined; fix when touching the file | off-scale spacing value, equal nested radii, missing tabular numerals |
| Nit | Optional taste; mention at most once | shadow could be layered, slightly long measure |

Contrast, target size, and screen-reader failures are reported with the severity assigned by accessibility-review, not re-scored here.

## Review approach

- Describe density, motion and variation in plain words (calm, balanced, dense), compared with the existing design system. Do not invent numeric scores.
- Redesign work starts with one question: preserve or overhaul? Audit the current tokens, navigation, content blocks and patterns worth keeping before suggesting change.
- Name what must not change silently: URLs and slugs, primary navigation labels, form field names and order, the logo, legal and consent text, analytics event names. Changing any needs explicit product owner approval (see information-architecture).
- Propose levers cheapest and safest first: type, spacing, colour balance, small motion, then larger recomposition. Stop when the brief is met.
- Read every visible string in the diff before sign-off: broken grammar, unclear referents, forced metaphors. Replace cute copy with a plain sentence.
- Mark placeholder data as placeholder. Never present invented figures, testimonials, logos or customer names as real.
- A list of ten rows with a divider under each is a flag; group, tabulate or disclose.
- Verify in light and dark at 375, 768 and 1440 as well as the widths in SKILL.md.

## Checklist

Fill each line with pass, fail, or n/a. A fail needs a row in the table or in "Not fixed". Do not mark pass for anything not examined; put it under "Could not verify".

```
Tokens
[ ] Design system inspected; existing tokens used for colour, spacing, radius, shadow, duration
[ ] No raw hex/rgb or arbitrary pixel values where a token exists
Surfaces and spacing
[ ] Spacing from the scale; gap inside groups smaller than between groups
[ ] Nested radii are concentric (outer = inner + padding)
[ ] Shadows only on floating layers; structure uses borders; borders low contrast
[ ] Icons optically aligned; images that blend into the surface have an outline
Motion
[ ] No transition: all / transition-all; properties named
[ ] Durations and easing match purpose; exits shorter than enters
[ ] Only transform and opacity animate for movement; no layout-shifting animation
[ ] No animation on high-frequency actions or first render
[ ] prefers-reduced-motion handled and tested
Typography and colour
[ ] Sizes and line heights from the scale; body measure about 45-75 characters
[ ] text-wrap balance on headings, pretty on body
[ ] Tabular numerals on changing or aligned numbers
[ ] Truncated text recoverable; flex children have min-w-0
[ ] Colours come from role tokens; dark theme uses its own tokens
[ ] Contrast pairs verified (accessibility-review)
Layout and states
[ ] Grouping, alignment, and reading order consistent with DOM order
[ ] Works at 320px, 768px, and wide desktop; no horizontal page scroll
[ ] Text can expand about 50% without clipping or overlap
[ ] Default, hover, focus-visible, active, disabled, loading, empty, error, success present where applicable
[ ] Forms: labels above, one control height, errors beside the cause
[ ] Hit areas adequate (accessibility-review)
Constraints
[ ] No new runtime dependency added
[ ] No scope creep; unrelated issues listed in one line each
[ ] Every visible string read; placeholder data marked as placeholder
```

## Could not verify

List every check that was not run, with the reason and what is needed. Typical entries:

- Rendering in a real browser (not available in this session).
- Dark theme or specific breakpoint not rendered.
- Reduced-motion behaviour not toggled.
- Real screen reader or touch device.
- Translated strings or very long user content.
- Exact contrast ratios and target sizes (hand to accessibility-review).
- Behaviour of a Tailwind or browser feature in a version not confirmed (state the version assumed).

If every item was verified, write "None" and state how (browser, widths, themes tested).

## Optional first pass

From this skill's folder, `python3 scripts/polish_scan.py <path>` lists lines that match the checkable rules in this skill (`transition: all`, removed focus outlines, heavy black shadows, text under 12px, hover-only reveals, looping motion with no reduced-motion rule, and the set of radii and z-index values in use). It reads source text only: treat each hit as a place to look, and a clean scan as no evidence. Add `polish-scan-ignore` in a comment to silence a line that is intentional.
