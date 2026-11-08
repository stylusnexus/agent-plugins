# iPad, Mac and Apple Watch

Source names: Apple Human Interface Guidelines (Designing for iPadOS, Multitasking, Sidebars, Designing for macOS, The menu bar, Windows, Keyboards, Pointing devices, Designing for watchOS, Digital Crown, Always On). Paraphrased; window and multitasking behaviour changed in recent iPadOS releases, so confirm against the OS you target.

## 1. iPad

- An iPad app is not a stretched iPhone app. Use the extra width for a sidebar, two or three columns, or a content area with a supporting pane.
- Layouts depend on size classes (compact or regular width and height), not on device name. The same window can be compact when narrow and regular when wide.
- Support multitasking and windowing. iPadOS 26 moved to free-form resizable windows, and the older Split View and Slide Over modes changed (Slide Over was removed, then returned in iPadOS 26.1 as a single-window mode; check the current HIG Multitasking page for the OS you target). Avoid assuming full screen, and avoid locking orientation. Content must reflow when the window resizes.
- Navigation: a sidebar suits many sections; it collapses to a tab bar or a hidden sidebar in a narrow window. Recent iPadOS releases let one tab bar convert to a sidebar; use the system component rather than building two separate navigation systems.
- Sheets and popovers: on iPad a popover usually anchors to the control that opened it; a form sheet appears centred. Do not show a full-width bottom sheet on a large window.
- Input: support hardware keyboards (focus, Tab, Return, Escape, shortcuts), pointer hover and the pointer shape, and drag and drop between apps where users move content.
- Targets stay finger-sized (44 pt default, 28 pt minimum on iPadOS) even though a pointer is more precise.
- Apple Pencil: if the app takes handwriting or drawing, allow it in text fields where the system supports it, and do not require a Pencil.

## 2. macOS

Mac users expect a menu bar, windows and the keyboard.

| Area | Convention |
|---|---|
| Menu bar | Every command lives in a menu, even if it also has a button. Use the standard menus in the usual order (app, File, Edit, View, Window, Help). Items not available are dimmed, not removed. Menu titles are verbs or nouns, with an ellipsis when more input is needed |
| Shortcuts | Use the standard ones for the standard commands (for example Command-N, -O, -W, -S, -Z, -C, -V, -F, -, for Settings, -Q). Do not reassign them. Show shortcuts in menu items |
| Windows | Resizable by default, remember size and position, support full screen where it makes sense, give each window a meaningful title. Use sheets for tasks that belong to one window, panels for tools |
| Toolbar | Frequent actions, search, view switching. Can be customized where users have different needs |
| Sidebar and inspector | Sidebar for navigation on the leading edge; inspector for properties of the selection on the trailing edge |
| Settings | One Settings window opened from the app menu, split into panes, applying changes immediately |
| Context menus | Right-click or Control-click menus for the item under the pointer. An accelerator only: the command must exist in the menu bar or toolbar too |
| Pointer and hover | Hover states, tooltips for icon-only controls, and the correct cursor. Hover hints are optional extras, never the only way to learn something |
| Undo | Undo and redo for edits, and for destructive actions where possible |
| Dock and menu bar extras | Add a Dock menu or a menu bar extra only when the app has value while in the background |

Control sizes on Mac are smaller than on touch devices (small, regular and large control sizes exist), because a pointer is precise. Do not enlarge controls to 44 pt on a Mac-only app. For Catalyst or other iPad-derived apps, check that spacing and menus were adapted, not carried over.

## 3. Apple Watch

- Design for a glance: a task takes seconds, text is short, and the main answer is on the first screen.
- Navigation uses vertical paging with the Digital Crown on current watchOS (not re-verified against the watchOS pages), and a stack for drill-in. Avoid deep hierarchies and long forms; hand off to iPhone for long input.
- Targets are large. Primary actions are full-width buttons; toolbar buttons sit in the corners. Check the exact sizes on the current Designing for watchOS pages.
- Use the Digital Crown for scrolling or adjusting a value, with haptic ticks that match.
- Always On display: reduce brightness, hide sensitive details when the wrist is down, and avoid fast animation.
- Complications and widgets in the Smart Stack are often the real entry point. Design them first for content that changes (next event, balance), and make tapping open the right screen.
- Notifications: short, actionable, with at most a few quick actions. Do not duplicate every iPhone alert.
- Dictation, scribble and quick replies beat typing. Give a choice list where you can.

## 4. One design, several Apple platforms

- Share the information structure and the vocabulary; do not share the chrome. A tab bar on iPhone can be a sidebar on iPad and Mac, and a short list on Watch.
- State per platform what changes: navigation, input, window behaviour, which features are reduced.
- Test each platform at its own extremes: iPhone at the largest text, iPad in the narrowest multitasking window, Mac window at minimum size, Watch at the largest text.

## 5. Review checks

- iPad: resize the window to its narrowest width; rotate; does layout reflow and nothing clip?
- iPad: can every function be used with a hardware keyboard?
- Mac: list every command and where it is in the menu bar. List any shortcut that overrides a standard one.
- Mac: does the window keep its size and position, and work at its minimum size?
- Watch: can the main task complete in about a few taps and no typing?
- Every platform: is there a visible alternative for every gesture, hover or context-menu-only action?
