# Touch targets, TalkBack, font scaling and other input

Source names: Android Developer documentation (Accessibility, Make apps more accessible, Touch target size, Compose accessibility semantics, Font scaling, Haptics, Keyboard input, Large screen app quality); Material Design 3 (Accessibility, Touch targets); the Accessibility Scanner app. Paraphrased. WCAG ratios and screen-reader behaviour in detail belong to accessibility-review.

## 1. Touch targets

- Android and Material guidance: at least 48 by 48 dp for anything tappable, with about 8dp between neighbouring targets. The visible icon can be smaller (a 24dp icon in a 48dp target).
- Use the component's built-in minimum touch target and do not turn it off to save space. In Compose, a small clickable may need extra padding or a minimum interactive size.
- Do not place two small targets inside one 48dp box.
- For WCAG on the web, 2.5.8 still sets the web minimum (24 CSS px). Cite which standard a finding uses.

## 2. TalkBack semantics (design level)

Specify these in the design so the build can follow them:

| Need | Specify |
|---|---|
| Name of an icon-only control | A short content description: the action, not the picture ("Delete invoice", not "Trash can icon") |
| Decorative image | Marked as decorative, so TalkBack skips it |
| Role and state | The role (button, switch, tab, checkbox) and state text for toggles, selection and expanded or collapsed |
| Headings | Section titles marked as headings so users can jump between them |
| Grouping | One announcement for a row (title, amount, status), with the row clickable as a unit and a separate target only for a distinct action |
| Custom actions | Swipe, long-press and drag actions exposed as custom accessibility actions |
| Dynamic changes | A live region or an announcement for results that appear without focus moving (for example "Invoice sent") |
| Order | Reading and focus order follow the visual order; modal content traps focus until dismissed |
| Errors | Error text linked to the field and announced when it appears |

Do not put role words in descriptions ("button"): TalkBack adds them. Do not rely on colour or position alone; say it in text.

Other services use the same semantics: Voice Access (speak the visible label to tap), Switch Access (scan or step through controls), and braille displays. A control whose spoken label differs from its visible label can be hard to say with Voice Access; keep them close.

## 3. System font scaling

- People set a font size and a display size in system settings. Newer Android versions scale large text up to about 200 percent and scale it non-linearly, so very large text grows less than small text. Confirm the current range in the docs.
- Use sp for text and dp for containers. Never lock text to a pixel height.
- Google's accessibility guidance asks for body text no smaller than 12sp.
- Test at the default, at a large setting and at the largest. At the largest, layouts should wrap or stack and nothing should be clipped or overlap.
- Icons and buttons that sit beside text may need to grow with the text.
- Display size (density) changes dp as well. Check that nothing relies on a fixed dp width.
- Navigation bar labels, chips and tabs are the usual first things to break; check them first.

## 4. Remove animations and other settings

- The "Remove animations" accessibility setting sets the system animation scale to zero. Apps that read it should replace large motion with an instant change or a fade.
- Also check: dark theme, colour correction and inversion, high-contrast text, bold text, and the touch and hold delay. Do not hard-code colours that fight these.
- Do not set a time limit on a task without a way to extend or turn it off. Timers on snackbars with actions should be long enough or the action available elsewhere.

## 5. Keyboards, mice, styluses

- Large-screen devices, ChromeOS and foldables are often used with a keyboard and pointer. Every function must work with Tab, arrow keys, Enter and Escape, with a visible focus indicator.
- Support common shortcuts (copy, paste, undo, find, save) where the app has those functions, and show a shortcut hint in menus.
- Mouse: hover states, right-click context menus (with the same commands available elsewhere), scroll wheel and drag.
- Stylus: if the app accepts handwriting or drawing, allow it in text fields where the system supports it, and do not require a stylus.
- Input method: set the right keyboard type and action key on each field (email, number, search), and do not block the system autofill.

## 6. Haptics

- Use the platform haptic constants for their meaning (confirm, reject, tick, long press) instead of raw vibration patterns, so feedback matches the rest of the system and honours the user's setting.
- Haptics confirm a result already visible; they never carry information alone.
- Newer versions add more feedback constants; check that a constant exists on your minimum API level.

## 7. Review checks

- Run the Accessibility Scanner and list each touch-target and label finding (a tool aid, not a substitute for manual TalkBack use).
- Walk the main flow with TalkBack on and note any unlabeled control or wrong reading order.
- View the main screens at the largest font scale and the largest display size; list what breaks.
- Turn on Remove animations; list the animations that remain large.
- Use only a keyboard on a tablet or emulator; list what cannot be reached.
