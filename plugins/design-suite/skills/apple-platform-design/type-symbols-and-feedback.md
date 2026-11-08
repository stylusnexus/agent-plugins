# Type, symbols, colour, haptics and motion

Source names: Apple Human Interface Guidelines (Typography, SF Symbols, Color, Dark Mode, Playing haptics, Motion, Accessibility, VoiceOver); SF Symbols app; Apple developer documentation for Dynamic Type. Paraphrased.

## 1. Dynamic Type

- Use the system text styles (large title, title, headline, body, callout, subheadline, footnote, caption) instead of fixed point sizes. Body defaults to 17 pt on iPhone; confirm the full table on the Typography page.
- People can raise text size in Settings, and further with the larger accessibility sizes. Design and test at the default, the largest standard size and the largest accessibility size.
- At the accessibility sizes, change the layout, not just the font. Side-by-side rows usually need to stack. Truncation is a last resort; let text wrap and let rows grow in height.
- Custom fonts are allowed but must scale with the text style (for example through the font metrics APIs). A custom font that ignores Dynamic Type is a finding.
- Scale spacing and icon sizes that sit next to text with the text.
- Avoid fixed-height containers for text. Do not hide information at large sizes.
- Keep text weight readable; respect Bold Text.

## 2. SF Symbols

- Prefer SF Symbols over custom icons for common actions. They match the system font's weight and scale with Dynamic Type.
- Match the symbol weight to nearby text. Use the same weight across a toolbar.
- Pick a rendering mode on purpose: monochrome, hierarchical, palette or multicolor. Use colour to add meaning, not decoration.
- Use the filled variant for the selected state in tab bars and the outline variant otherwise, as the system does.
- Check that the symbol exists on the minimum OS you support. Symbol availability depends on the OS version, and the SF Symbols app lists it. The current symbol set version is not stated here because it may be out of date.
- Custom symbols should follow the SF Symbols template so they align and scale. Do not use Apple's marks or SF Symbols for app icons or logos; check the licence terms.
- Every icon-only control needs an accessibility label (see section 6).

## 3. Colour and dark mode

- Use semantic and system colours (label, secondary label, system background, separators, tint) so light, dark and increased contrast variants come for free.
- Provide light and dark variants for any custom colour. Check images and shadows in dark mode.
- Use one tint colour for interactive elements. Do not use colour as the only signal of state; respect Differentiate Without Color.
- Honour Increase Contrast and Reduce Transparency: translucent materials must still leave text readable. Exact ratios belong to accessibility-review.
- Do not recolour system controls to look custom if it breaks their states.

## 4. Haptics

- Haptics confirm what just happened. They never carry information that is not also shown or announced.
- Use the system feedback types for their meaning: impact for a physical collision or snap, selection for moving through values, notification for success, warning or error.
- Use them sparingly. Constant buzzing on scroll or tap is noise, and people can turn system haptics off.
- Pair custom haptics with the same moment in sound and visuals so they feel like one event.
- Not every device has the hardware (most iPads have none; check the target devices).

## 5. Motion and Reduce Motion

- Use motion to explain a change (where something came from or went), not to decorate.
- Keep transitions short and interruptible. Do not block input while an animation plays.
- When Reduce Motion is on: replace large movement, zooms, parallax, spinning and auto-playing animation with a cross-fade or no animation. Keep small state changes.
- Also consider the Prefer Cross-Fade Transitions option and auto-playing video settings.
- Do not remove feedback; swap the motion for another cue.

## 6. VoiceOver naming and order (design level)

VoiceOver testing and exact screen-reader behaviour belong to accessibility-review. A design should still specify:

- A label for every control that has no visible text. Labels are short nouns or verbs and do not repeat the control type ("Delete", not "Delete button").
- A value for controls with state (sliders, toggles, steppers) and a trait for what the element is (button, header, selected).
- Hints only where the result of an action is not clear from the label; keep them short.
- Reading order that follows the visual order; group related text into one element (price and unit together).
- Custom actions for swipe-only or long-press-only actions.
- Announcements for important changes that happen without focus moving (for example "Invoice sent").
- Decorative images are hidden from VoiceOver.

## 7. Review checks

- View each screen at the largest accessibility text size; list what breaks.
- Toggle dark mode, Increase Contrast and Reduce Transparency; list what breaks.
- Turn on Reduce Motion; list each animation that remains large.
- List every icon-only control and its accessibility label.
- List each haptic and the moment it fires; confirm nothing depends on it alone.
