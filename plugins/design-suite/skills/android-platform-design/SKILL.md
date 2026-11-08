---
name: android-platform-design
description: "Use when designing or reviewing an interface for Android and Google platforms against Material Design 3 and the Android developer docs: navigation bar, rail and drawer, edge-to-edge and window insets, predictive back, adaptive layouts and window size classes for phones, tablets and foldables, dynamic color, 48dp touch targets, TalkBack, system font scaling, snackbars, permissions."
---

# Android platform design

Review or shape a design so it behaves the way people expect on Android phones, tablets, foldables and ChromeOS. Follow Material Design 3 and the platform's system behaviour unless the product has a reason to differ, and say what that reason is. This is an AI design perspective based on published guidance, not device testing, Play review advice or user research.

## When to use

- A native or cross-platform app is shipping on Android, or a web or iOS design must be adapted to it.
- A review asks "does this follow Material?" or "will this survive the latest Android version?".
- Choosing navigation, back behaviour, layout across screen sizes, colour theming or feedback for an Android screen.

Not for: platform-neutral touch, offline and responsive-web rules (use mobile-design); exact contrast ratios and screen-reader testing (use accessibility-review); iOS, iPadOS, macOS or watchOS (use apple-platform-design).

## Workflow

1. Identify the target and minimum API level, UI toolkit (Jetpack Compose, Views, cross-platform toolkit), form factors and evidence. Mark unknowns MISSING INFORMATION. System behaviour changes by Android version and by target SDK, so state the versions the review assumes.
2. Inspect existing screens, theme and components. Prefer Material components over custom ones.
3. Check structure and back (`navigation-and-adaptive-layout.md`): navigation bar, rail and drawer by window size, edge-to-edge, system bars and gestures, predictive back.
4. Check the visual system and feedback (`material-theme-and-components.md`): dynamic color, type scale and font scaling, shape, motion, snackbars, dialogs, sheets, permissions.
5. Check accessibility hooks at design level (`talkback-and-input.md`): 48dp targets, TalkBack names and order, font scale, remove-animations, other input methods. Send exact ratios and assistive-technology testing to accessibility-review.
6. Return findings with the platform source named by title, severity, and a fix.

## Reference files

| File | Open when |
|---|---|
| `navigation-and-adaptive-layout.md` | Choosing bar, rail or drawer, window size classes, foldables, edge-to-edge insets, system gestures, predictive back |
| `material-theme-and-components.md` | Dynamic color, type and shape, app bars, FAB, sheets, dialogs, snackbars, motion, permissions and notifications |
| `talkback-and-input.md` | Touch targets, TalkBack semantics, font scaling, remove animations, keyboard, haptics, Switch Access and Voice Access |

## Output format

Label the result "Expert review against Material Design 3 and Android developer guidance, versions assumed: ...". Per screen or flow: window size class, findings (each: observation, guideline area, severity, fix, evidence: VERIFIED from source or screenshot, or NEEDS-TEST on a device), then Trade-offs, Open questions, and a **Checks not performed** list (for example: not run on a device or emulator, TalkBack not used, largest font scale not viewed, no foldable or tablet tested, gesture and three-button navigation not both tried, Play policy not assessed).

## Boundaries

- Cite Material Design 3, Android Developer documentation and the large-screen app quality guidance by title only. Paraphrase; do not paste guideline text.
- Where a number, API name or version is uncertain, say so and point to the current documentation rather than guessing.
- The 48dp target and similar values are platform guidance. WCAG 2.5.8 remains the web minimum; accessibility-review owns exact targets and ratios.
- Material is a default, not a law. Brand, pricing, priority and any decision to depart from the platform stay with product owners.
- Do not claim Play Store approval or policy compliance. Policies and target-SDK deadlines change; point to the current Play Console and Android docs.
- Do not add a dependency or switch UI toolkit unless asked. Do not publish, merge, deploy or contact users.
- Respect the project's licensing constraints, including Google's terms for Material icons, fonts and marks.
