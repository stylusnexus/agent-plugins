---
name: mobile-design
description: "Use when designing or reviewing mobile, responsive or small-screen interfaces: touch targets, thumb reach, bottom bar or drawer navigation, back behaviour, gestures, mobile forms and keyboards, viewport and safe-area handling, slow or offline networks, layout shift, reduced motion. Also for deciding whether a responsive web experience is enough versus a native app."
---

# Mobile design

Design around the user's context and task on small screens: constrained width, touch, interruptions, connectivity and input methods. Do not assume a native app is required when a responsive web experience fits. This is an AI design perspective, not device analytics or user research.

## When to use

- A flow or screen that must work on phones or small windows.
- Adapting a desktop layout, table or dashboard to narrow widths.
- Mobile forms, navigation, or touch interaction problems.
- Slow-network, offline or interrupted-task behaviour.

## Workflow

1. Identify user, task, device context and evidence. Mark unknowns MISSING INFORMATION (device mix, connectivity, one-handed use are all unknown unless supplied).
2. Inspect existing breakpoints, components and mobile behaviour in code or screenshots.
3. Prioritise content and actions; do not shrink a desktop layout into a narrow viewport.
4. Specify navigation, touch targets, text scaling, keyboard behaviour, orientation and reflow, and long-content handling (`touch-and-navigation.md`, `responsive-and-input.md`).
5. Specify loading, error, slow-network, offline and interrupted-task behaviour, plus motion and layout stability (`performance-and-offline.md`).
6. Coordinate with the dashboard designer for dense data and the accessibility expert for inclusive interaction.
7. Return annotated mobile states, responsive rules, trade-offs and acceptance criteria.

## Reference files

| File | Open when |
|---|---|
| `touch-and-navigation.md` | Sizing and spacing controls, thumb reach, choosing navigation pattern, back behaviour, gestures |
| `responsive-and-input.md` | Writing responsive CSS rules, viewport units, safe areas, forms, input types, keyboards, orientation |
| `performance-and-offline.md` | Slow or no network, images, tap latency, layout shift, motion and reduced motion |

## Output format

Per screen: purpose, priority order of content, layout at narrow, medium, wide, controls with target sizes, navigation and back behaviour, states (empty, loading, partial, error, success, offline, permission-denied; see the ui-ux skill's state list), input types and keyboard behaviour. Then trade-offs, open questions, and acceptance criteria that can be checked at a stated viewport (for example 320 CSS px wide, 200% text size).

## Boundaries

- Do not assume device analytics, audience devices or customer research; ask or mark MISSING INFORMATION.
- Platform values (Apple 44 pt, Material 48 dp) are platform guidance; WCAG 2.5.8 is the web minimum. Cite which is meant.
- Numbers labelled "recommended" are defaults for product owner confirmation, not measurements.
- Product owners keep product, pricing, priority and the web-versus-native decision. Do not propose a native app, new dependency or design system unless asked.
- Preserve source-of-truth and privacy boundaries (location, camera, notification and contact permissions need a stated reason).
- Do not publish, merge, deploy or contact users.
- Respect the project's licensing and attribution constraints for any content shown.
