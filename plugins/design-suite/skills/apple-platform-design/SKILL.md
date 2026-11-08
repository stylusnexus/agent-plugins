---
name: apple-platform-design
description: "Use when designing or reviewing an interface for Apple platforms (iOS, iPadOS, macOS, watchOS) against the Human Interface Guidelines: tab bars, navigation stacks, sheets and alerts, SF Symbols, Dynamic Type, safe areas, system gestures, haptics, iPad multitasking and sidebars, macOS menu bar, windows and keyboard shortcuts, watchOS glanceable screens, VoiceOver and Reduce Motion handling, dark mode."
---

# Apple platform design

Review or shape a design so it behaves the way people expect on iPhone, iPad, Mac and Apple Watch. Follow the platform's conventions unless the product has a reason to differ, and say what that reason is. This is an AI design perspective based on Apple's published guidance, not App Review advice, device testing or user research.

## When to use

- A native or cross-platform app is shipping on iOS, iPadOS, macOS or watchOS.
- A web or Android design must be adapted to an Apple platform.
- A review asks "does this feel native?" or "will this pass a Human Interface Guidelines check?".
- Choosing navigation, modality, icons, type or feedback for an Apple screen.

Not for: platform-neutral touch, offline and responsive-web rules (use mobile-design); exact contrast ratios and screen-reader testing (use accessibility-review); Android or Material (use android-platform-design).

## Workflow

1. Identify the platforms, minimum OS version, UI framework (SwiftUI, UIKit, AppKit, cross-platform toolkit) and evidence. Mark unknowns MISSING INFORMATION. Guidance changes between OS releases (the 2025 releases introduced a new visual material), so state which OS the review assumes.
2. Inspect the existing screens, components and any design system. Prefer system components over custom ones.
3. Check structure and navigation (`ios-navigation-and-modality.md`): tab bar, navigation stack, sheets, alerts, menus, and the iPad and Mac forms of each.
4. Check visual system and feedback (`type-symbols-and-feedback.md`): Dynamic Type, SF Symbols, colour and dark mode, haptics, motion.
5. Check platform-specific shells (`ipad-mac-watch.md`): size classes and multitasking, macOS menu bar, windows and shortcuts, watchOS glanceability.
6. Check accessibility hooks at design level (VoiceOver labels and order, Reduce Motion, larger text). Send exact ratios and assistive-technology testing to accessibility-review.
7. Return findings with the platform source named by title, severity, and a fix.

## Reference files

| File | Open when |
|---|---|
| `ios-navigation-and-modality.md` | Tab bar versus other navigation, navigation bars, back gesture, sheets and detents, alerts, action menus, safe areas, permissions |
| `type-symbols-and-feedback.md` | Dynamic Type, SF Symbols, system colours and dark mode, haptics, Reduce Motion, VoiceOver naming |
| `ipad-mac-watch.md` | iPad layouts, windowing, sidebars, macOS menu bar, windows, shortcuts, pointer, watchOS screens |

## Output format

Label the result "Expert review against Apple Human Interface Guidelines, OS assumed: ...". Per screen or flow: platform and form factor, findings (each: observation, guideline area, severity, fix, evidence: VERIFIED from source or screenshot, or NEEDS-TEST on a device), then Trade-offs, Open questions, and a **Checks not performed** list (for example: not run on a device or simulator, VoiceOver not used, Dynamic Type largest sizes not viewed, Reduce Motion not toggled, App Review not assessed).

## Boundaries

- Cite Apple Human Interface Guidelines, the SF Symbols app and Apple developer documentation by title only. Paraphrase; do not paste guideline text.
- Where a number or API name is uncertain, say so and point to the current Human Interface Guidelines page rather than guessing.
- Scope: iOS, iPadOS, macOS and watchOS. visionOS and tvOS are not covered; the 2025 Liquid Glass redesign (floating tab bars and toolbars, minimize on scroll, search as a tab role) is only touched on, so check the HIG for the OS you target.
- The 44 pt default (28 pt minimum) and similar values are platform guidance. WCAG 2.5.8 remains the web minimum; accessibility-review owns exact targets and ratios.
- Native conventions are a default, not a law. Product owners keep brand, pricing, priority and any decision to depart from the platform.
- Do not claim App Store approval or compliance. Review rules change; point to the current App Review Guidelines for submission questions.
- Do not add a dependency or switch UI framework unless asked. Do not publish, merge, deploy or contact users.
- Respect the project's licensing constraints, including Apple's terms for SF Symbols and Apple marks.
