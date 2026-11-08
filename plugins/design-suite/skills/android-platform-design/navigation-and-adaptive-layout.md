# Navigation, adaptive layout, edge-to-edge and back

Source names: Material Design 3 (Navigation bar, Navigation rail, Navigation drawer, Canonical layouts, Applying layout); Android Developer documentation (Window size classes, Build adaptive apps, Edge-to-edge, Handle window insets, Predictive back, Large screen app quality). Paraphrased. Version details move fast; confirm against the current docs.

## 1. Window size classes first

Design by the size of the window, not the device type. A phone, an unfolded foldable, a tablet and a resized window on ChromeOS or in split screen can all land in any class.

| Width class | Approximate width | Typical navigation |
|---|---|---|
| Compact | under 600dp | Navigation bar at the bottom; single pane |
| Medium | 600dp to under 840dp | Navigation rail; one or two panes |
| Expanded | 840dp to under 1200dp | Navigation rail or a standard drawer; two panes |
| Large | 1200dp to under 1600dp | Rail or drawer; two or three panes. Needs the adaptive library's large-width support switched on |
| Extra-large | 1600dp and wider | Aimed at desktop-class displays; cap content width and use more panes |

Height classes also exist: compact under 480dp, medium 480dp to under 900dp, expanded 900dp and up. A phone in landscape is often compact in height, so avoid tall fixed headers. (Breakpoints checked against the Android "Use window size classes" page on 2026-11-08.)

Rules:

- Do not lock orientation or assume a fixed window. For apps that target Android 16 (API 36), orientation, resizability and aspect-ratio restrictions are ignored on displays whose smallest width is 600dp or more (games are exempt). A temporary opt-out exists for API 36, and it is removed for apps that target Android 17 (API 37). An app that cannot resize will be letterboxed or break. Verify the behaviour for the target SDK you ship in the current docs. Google Play also requires new apps and updates to target a recent API level on a published schedule (as of 2026-11 that was API 36 for most apps); check the Play Console help page for the current deadline.
- Use the three canonical layouts where they fit: list-detail (master list plus content), supporting pane (main content plus related content), feed (a grid or list that changes column count).
- Content width: on wide windows, cap line length and keep forms readable instead of stretching to the full width.
- Foldables: a hinge or fold can split the screen. Keep important controls out of the fold and consider tabletop posture for media and camera. Use the window manager APIs to read posture instead of guessing.

## 2. Choosing navigation

| Pattern | Good when | Cautions |
|---|---|---|
| Navigation bar | 3 to 5 equal top-level destinations on compact widths | Labels on every item; one clear active state; badges only for real counts; not for actions |
| Navigation rail | Medium and larger windows, 3 to 7 destinations | Optional menu button and a FAB or primary action at the top. Do not keep a bottom bar next to a rail |
| Navigation drawer | Many destinations or a deep top level; expanded windows can use a permanent drawer. Material 3 Expressive favours an expanded navigation rail instead; follow whichever the project uses | On compact it is a modal drawer that hides options; use it for secondary destinations, not the only route to a core task |
| Top app bar | Title, up button and contextual actions for the current screen | Keep a few actions; overflow the rest into a menu |
| Tabs | Switching views of the same content | Not for top-level destinations; do not nest tab sets |
| Search bar | Large content sets | Show recents and suggestions; keep scope clear |

Use a navigation component that swaps between bar, rail and drawer as the window changes, rather than three hand-built versions. The Material 3 adaptive libraries provide scaffolds for this.

Up and back differ: Up (top app bar arrow) goes to the parent in the app's hierarchy; Back follows history. They agree in a simple stack and differ after deep links or from a different task. A deep link should open with a sensible parent behind it.

## 3. Edge-to-edge and system bars

- Apps draw behind the status bar and navigation bar. Edge-to-edge is enforced for apps that target API 35 (Android 15) or higher, and the opt-out attribute stops working for apps that target API 36 on Android 16 and later. Treat it as the default design, not an option.
- Handle window insets: system bars, display cutout, system gestures and the on-screen keyboard (IME). Content scrolls behind the bars; controls and text must not sit under them.
- Make bar backgrounds transparent or scrim them so icons stay legible over content; the system chooses icon contrast for three-button navigation with a scrim.
- Put the primary bottom action above the gesture bar and above the keyboard, with insets applied.
- Material scaffolds and bars apply many insets for you. Custom screens need to apply them on purpose; a finding is "content hidden under the navigation bar" or "button under the keyboard".

## 4. System gestures

- Gesture navigation: swipe from either side edge for back; from the bottom for home and recents. Three-button navigation still exists. Test both.
- Do not put a horizontal swipe, slider, carousel edge or drawer handle at the screen edges. Drawers open with a visible menu button first; edge-drag is an extra.
- Apps can exclude small edge regions for gestures, but the allowance is limited and discouraged. Prefer moving the control.
- Every gesture action needs a visible alternative: a button or menu item.

## 5. Predictive back

- Predictive back shows a preview of where back will go as the user drags, then commits or cancels. It rolled out across several Android versions: first behind a developer option (Android 13 and 14), then as an opt-in for apps (Android 15). For apps that target API 36 on Android 16 and later it is on by default, and the old back key callbacks are no longer delivered. Check the current docs for the target SDK you ship.
- Use the supported back APIs (the AndroidX back callback and, in Compose, the back handlers). Do not intercept the raw back key press or override the old back method; those prevent the preview or are ignored on newer versions.
- Design for the system animations: back to home, between activities, between tasks, and in-app. Custom in-app transitions should be interruptible and use the same progress as the gesture.
- Back must never discard unsaved input silently. If you intercept back, show a clear choice (keep editing or discard).
- Do not use back to trap the user or to bounce through a redirect loop. After a finished flow, back goes to the result.
- Back dismisses the topmost thing first: keyboard, then sheet or dialog or menu, then the screen.

## 6. Review checks

- Name the window size class for each layout and the navigation pattern used in it.
- Resize the window (split screen, tablet, fold open and closed); does the layout reflow?
- Rotate; is orientation locked anywhere?
- Is anything hidden under the status bar, gesture bar, cutout or keyboard?
- Try both gesture and three-button navigation.
- Does back dismiss sheets and dialogs before leaving the screen, and does predictive back preview work?
- Is each gesture backed by a visible control?
