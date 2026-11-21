# Touch zones, targets and screen structure

Complements `touch-and-navigation.md`. Numbers marked "recommended" are defaults for product owner confirmation. Test population and device mix for any figure below are unknown unless the source states them; mark MISSING INFORMATION.

## 1. Centre-out placement

This centre-out model is an alternative to the thumb-reach model in `touch-and-navigation.md`. Name which one the review applies; do not mix them on one screen.

- Put primary actions in the middle band of the screen (roughly the middle half to two thirds, recommended) and edges for secondary items. Check: mark the band on a screenshot; every primary action sits inside it.
- Three-zone template: primary content or function in the centre, secondary controls as edge buttons or tabs, tertiary items in a corner menu. Check: top-level navigation is visible in the centre or edge, not only inside a menu.

## 2. Target size by zone

| Zone | Recommended physical size | Status |
|---|---|---|
| Centre | about 7 mm | Recommended default |
| Edges and corners | about 12 mm | Recommended default |

- Edge and corner taps land less accurately, so those targets need to be larger. Check: measure targets in millimetres on a real device, not only in CSS px.
- Do not cite these as standards. Test population and conditions for the research behind them are not recorded here; mark NEEDS-TEST for this product.

## 3. Hit radius and cost of a miss

- Size each target so most taps land inside it (a design goal near 95 percent, recommended); accept that some will miss. Check: for each control, name what a miss next to it triggers. If the neighbour is destructive, add distance or confirmation-by-undo.
- Make whole containers tappable: the entire row, card or button, never a bare word or icon. Check: every label sits inside a bounded tappable area at least row-sized.
- Keep Delete at least one slot away from Save and other frequent actions.
- Prefer undo over a confirmation dialog for reversible actions; keep dialogs for truly critical steps. Check: each delete or remove has undo or a restore path within the session.

## 4. Feedback and edges

- A tap changes state in the same moment, and the change is visible around a fingertip. Check: record the tap on a device; the pressed state is larger than the finger footprint and shows without lifting.
- Keep interactive items clear of the outer margin: system gestures, phone cases and browser bars take the edges. Check: no tappable item within the OS gesture zones at top, bottom or sides; test with gesture navigation on.

## 5. Encode every meaning twice

- Pair icons with text labels; never rely on colour alone. Check: convert a screenshot to greyscale; every state (selected, error, success, disabled) is still distinguishable.
- Important notices (errors, warnings, anything affecting money or data) stay until dismissed. Check: no essential message disappears on a timer.
- Size type by viewing distance and device class; type tokens differ for phone and tablet. Check: tokens are defined per device class, and the smallest text is checked on a real device at arm's length.

## 6. Hierarchy order

- Rank emphasis by position first, then size, shape, contrast, colour. Check: squint test on a blurred screenshot gives the same ranking as the intended one.

## 7. Disclosure fit

| Pattern | Fit |
|---|---|
| Tabs | At the top; 3 to 5 (recommended) |
| Accordion | One section open at a time |
| Drawer | Stays docked to its origin |
| Pop-up | Weak for drill-down; avoid for it |

Check: each disclosure matches the task, and the tab count is within range.

## 8. Controls and components (recommended defaults)

- Bottom tabs: at most 5. Check: count.
- Form fields per step: about 7 to 8 on desktop, 3 to 4 on phone; split longer forms. Check: count visible fields per step.
- Tables on phones: keep the 3 to 5 key columns visible at 375 px, with a way to reach the rest, or reshape rows into cards. Check: render at 375 px.
- Sliders: pair with +/- steppers and a text field for exact entry; announce value changes to screen readers. Check: enter an exact value without dragging.
- Carousels: no auto-rotation by default (see `component-patterns.md` in accessibility-review). If the product owner requires it: advance no faster than 5 to 7 s (recommended), visible pause control (2.2.2), stops on interaction, off under reduced motion and on phones. Check: leave the page idle on a phone and confirm nothing rotates.

## 9. Grips and conditions

- Users cradle, hold with one hand, or use two hands, and switch between them. Check: the primary action is reachable from cradle and one-handed grips; grip mix for this audience is MISSING INFORMATION.
- Stress test glare, noise, motion and distraction. Check: no cue depends on audio alone or colour alone; primary targets are still hittable while walking.
- Review on a real device. Check: every screen has been read and tapped on a physical phone, with sizes measured on screen. Desktop previews misjudge touch.

## 10. Where a rule came from

Button-size guidance disagrees across sources (reported figures range from under 10 mm to over 20 mm). Check: each cited sizing rule states its source, unit and test population; if it cannot, label it recommended and move on. List real-device measurement and grip testing under "checks not performed" when skipped. This is expert review, not user research.

Sources: Touch Design for Mobile Interfaces (Steven Hoober); Smart Interface Design Patterns Checklists (Vitaly Friedman).
