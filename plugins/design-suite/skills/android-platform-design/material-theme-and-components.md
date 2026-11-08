# Material 3 theme, components, motion and permissions

Source names: Material Design 3 (Color system, Dynamic color, Typography, Shape, Elevation, Motion, App bars, Buttons, Dialogs, Bottom sheets, Snackbar, Chips); Android Developer documentation (Runtime permissions, Notification runtime permission, Photo picker, Splash screen, Per-app language). Paraphrased. Material has had expressive updates since 2025; check which Material version the project actually uses before judging a screen against the other.

## 1. Dynamic color and theming

- Dynamic color builds the app palette from the user's wallpaper on Android 12 and later. Using it makes the app feel at home and respects the user's choice.
- Always provide a static brand scheme as the fallback for older versions and for any user who turns dynamic color off. A product with strict brand colour can choose the static scheme; that is a product decision.
- Use colour roles, not hex values, in components: primary, on-primary, primary container, secondary, tertiary, surface and its container levels, outline, error. Pair each role with its "on" colour so contrast is built in.
- Define both light and dark schemes and respect the system setting. Do not hard-code white or black.
- Check brand-critical content (logos, status colours such as success or warning) separately; dynamic roles can change hue. Use custom colour roles harmonized with the scheme for status.
- Do not mix Material 2 and Material 3 components on one screen.
- Themed app icons (Android 13 and later) need a monochrome icon layer. Confirm it exists.

## 2. Type, shape and elevation

- Use the Material type scale (display, headline, title, body, label; each large, medium, small) via theme tokens, not per-screen sizes.
- Text sizes are in sp so they follow the user's font size setting. See `talkback-and-input.md` for scaling tests.
- Use shape tokens for corner radii and keep one shape language across the app.
- Material 3 shows depth with tonal surface colour more than shadow. Do not stack heavy shadows on top of it.

## 3. Components

| Need | Use | Notes |
|---|---|---|
| Screen title, up button, actions | Top app bar (small, centred, medium or large) | A few actions, then an overflow menu. Collapsing bars should keep the title readable at large font scale |
| Primary action on a screen | One FAB or extended FAB, or a filled button | One primary action per screen. Do not place a FAB over content it hides without a scroll-away behaviour |
| Choices and filters | Chips, segmented buttons | Keep labels short; filters should show the selected state clearly |
| Short contextual choices | Modal bottom sheet or menu | Sheets need a visible dismiss route, a drag handle where draggable, and back support |
| Persistent supporting content | Standard bottom sheet or side sheet | On wide windows prefer a side sheet |
| Decision that blocks the user | Dialog | Title and verb buttons ("Delete", not "OK"); at most two or three actions; full-screen dialog for multi-field tasks on compact windows |
| Brief feedback after an action | Snackbar | Short text, one optional action such as Undo, auto-dismiss, anchored above the bottom bar or FAB. Do not use it for errors the user must act on |

- Prefer a snackbar with Undo over a confirmation dialog for reversible deletes. Use a dialog only when the action cannot be undone.
- Avoid the legacy toast for in-app feedback; the platform limits it and it cannot carry an action.
- Pull to refresh, swipe to dismiss and long-press selection are accelerators. Each needs a visible equivalent.

## 4. Motion

- Material motion patterns: container transform (an item becomes its detail), shared axis (siblings in a sequence), fade through (unrelated destinations), fade (small elements). Pick the one that explains the relationship. (These names come from the Material transition patterns. Material 3 Expressive also adds spring-based motion; check the current motion page for which a given project uses.)
- Keep durations short and interruptible. Match predictive back progress to the animation.
- Respect the system setting that removes animations (the animation scale set to zero, exposed as "Remove animations" in accessibility settings): replace movement with an instant change or a plain fade, and keep feedback.
- Do not rely on animation to tell the user something happened.

## 5. Permissions and notifications

- Ask for a runtime permission at the moment the feature needs it, after a plain-language reason. Request the narrowest permission.
- Prefer system pickers over broad permissions: the photo picker and document picker need no storage permission; one-time and approximate location are options. Newer versions also allow partial photo access.
- The user can deny, deny twice (the system then stops asking), or grant for one use. Design the denied state: the feature explains what is missing and offers a path to settings.
- Notifications use channels that the user can turn off one by one; name and describe channels clearly. Newer versions require a runtime permission to post notifications; ask after the user sees value, not at first launch.
- Do not use notifications for ads or for things that do not need attention.

## 6. Startup and language

- Use the platform splash screen API with the app icon and a plain background colour. A custom full-screen splash adds a second splash on newer versions.
- Per-app language lets users pick the app language in system settings (Android 13 and later). Declare supported locales and test layout with long strings and right-to-left languages.

## 7. Review checks

- Does the screen use theme roles and tokens, and does it work in light, dark and with dynamic color on and off?
- Is the Material version consistent across the screen?
- Is there exactly one primary action, and does it avoid covering content?
- Are reversible actions handled by Undo and irreversible ones by a clear dialog?
- Does each permission request have context, a denied state and a path to settings?
- With animations removed, does the flow still communicate state?
