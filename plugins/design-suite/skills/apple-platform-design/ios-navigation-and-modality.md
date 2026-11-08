# iOS navigation, modality and safe areas

Source names: Apple Human Interface Guidelines (Tab bars, Navigation bars, Sheets, Alerts, Layout, Gestures, Privacy). Paraphrased; confirm exact values on the current pages.

## 1. Choosing the main structure

| Pattern | Good when | Cautions |
|---|---|---|
| Tab bar | A few top-level sections people switch between often | Use it for places, never for actions. Keep tab roles stable. Each tab keeps its own navigation history. On iPhone only about five tabs fit before a "More" tab appears, so plan for four or five at most |
| Navigation stack (navigation bar) | Drilling from a list into detail | Title says where you are. The back button is top leading and carries the previous title. Do not replace it with a custom control |
| Sidebar (iPad, Mac) | Many sections or a deep hierarchy | See `ipad-mac-watch.md` |
| Page control or paging | A small, ordered set such as onboarding | Not for primary navigation |
| Search | Large catalogues | Use the system search field; keep recents; scope when the data is mixed |

Do not make a hamburger menu the main navigation on iOS. People can still use one for secondary items, but it hides destinations that a tab bar would show.

Recent OS releases changed how the tab bar and toolbars look (floating bar, search placed in the bar, a bar that shrinks while scrolling). Build with the system components so the app picks up the current look; check the Tab bars page for the OS you target.

## 2. Navigation bar and back

- Large titles suit the root of a section; inline titles suit deeper screens. Let the system collapse the title on scroll.
- Put at most a few trailing actions in the bar. More than that belongs in a menu behind a "More" (ellipsis) button.
- The edge swipe from the leading side goes back. Do not place a horizontal carousel, slider or drawer at the screen edge that fights it. If a screen must block the swipe (unsaved changes), warn the user instead of silently trapping them.
- Back returns to the same scroll position and filters. After a completed flow, go to the result, not to a stale form.

## 3. Sheets and modality

- Use a sheet for a self-contained task or a short choice. Use a push for moving deeper in the same content.
- Sheets can rest at partial heights (detents, commonly medium and large). Use a partial height when the content behind still matters. Show the grabber when the sheet is resizable.
- Every sheet needs a clear way out: swipe down, and a Cancel or Done button. When unsaved input would be lost, intercept the swipe-down and ask first (a confirmation menu with a destructive Discard option).
- Cancel sits at the leading edge, Done or Save at the trailing edge. Make the affirmative action the prominent one.
- Do not stack sheets on sheets. Do not use a full-screen cover unless the task is truly immersive (camera, onboarding, sign-in).

## 4. Alerts, confirmations and menus

| Need | Use |
|---|---|
| Important news that needs a decision | Alert, with a short title and one or two buttons |
| Choose among actions for something the user just picked | Confirmation dialog (action sheet on iPhone, popover on iPad) |
| Secondary actions on an item | Context menu (long press), plus a visible route to the same action |
| Quick row actions | Swipe actions, plus the same actions inside the item or a menu |
| Brief, non-blocking feedback | Inline status or a banner you build; avoid alerts for success |

- Alert titles say what happened or what will happen; buttons use verbs ("Delete Invoice", not "OK").
- Mark destructive buttons with the destructive style. Do not make the destructive choice the default.
- Never rely on long press or swipe alone: they are not discoverable and are hard for assistive technology users.

## 5. Safe areas and layout

- Keep content and tappable controls inside the safe area. Let backgrounds, images and scrolling content extend behind the bars and the home indicator.
- Respect the Dynamic Island and camera cutout, the status bar and the home indicator. Do not place buttons on the bottom edge so they collide with the home indicator.
- Use the system layout margins and readable content width instead of fixed point values, so layouts fit every iPhone, iPad and orientation.
- Handle the keyboard: scroll the focused field into view and keep the primary action reachable.
- Touch targets: 44 by 44 pt minimum is Apple's figure. Pad the hit area, not the icon.

## 6. Permissions and sign-in

- Ask for a permission in context, at the moment the feature needs it, after a short explanation of the benefit. Write the purpose string in plain language.
- If the user declines, the app still works as far as possible and offers a path to Settings later.
- If the app offers third-party sign-in, check the current App Review Guidelines for the rule about also offering a privacy-preserving option such as Sign in with Apple. The exact wording is not quoted here and may have changed; verify before relying on it.

## 7. Review checks

- Is the structure a tab bar, stack or sidebar chosen for the number and frequency of destinations?
- Does the back swipe work on every pushed screen?
- Does every sheet have an exit and a guard for unsaved input?
- Is every gesture action also reachable by a visible control?
- Are destructive actions labelled with verbs and styled as destructive?
- Do bottom controls clear the home indicator and the keyboard?
- Is every permission request preceded by context?
