# Forms and errors

Related criteria: 1.3.1, 1.3.5, 3.3.1, 3.3.2, 3.3.3, 3.3.4, 3.3.7 (new in 2.2), 3.3.8 (new in 2.2), 4.1.3.

## Labels and instructions (3.3.2, A)

Every input has a visible, persistent label that is programmatically associated.
```tsx
const id = useId();
<label htmlFor={id}>Email</label>
<input id={id} name="email" type="email" autoComplete="email" aria-describedby={`${id}-hint`} />
<p id={`${id}-hint`}>We only use this for receipts.</p>
```
- Fail patterns: placeholder as the only label; label not associated (`<label>` with no `htmlFor`/nesting); `aria-label` only on a field whose visible text differs (also 2.5.3); labels positioned so the mapping is ambiguous.
- No floating labels that shrink into the placeholder; keep the label visible above the field.
- Instructions (format, limits) go in persistent text linked by `aria-describedby`, before the user needs them. Not in a tooltip alone.
- Required: mark with visible text or an asterisk explained at the form top, plus the native `required` attribute (or `aria-required="true"` when using custom validation). Color alone is not enough.
- Use the correct `type` (`email`, `tel`, `url`, `number`) and `inputMode` so the right keyboard appears. Avoid `type="number"` for IDs, postal codes, and card numbers (spinner and wheel behavior, no leading zeros); use `inputMode="numeric"` with `pattern`.
- Do not disable paste on any field.

## Grouping

Related controls (radio sets, checkbox groups, address blocks, date parts) use `fieldset` with `legend`:
```html
<fieldset>
  <legend>Notification method</legend>
  <label><input type="radio" name="notify" value="email"> Email</label>
  <label><input type="radio" name="notify" value="sms"> Text message</label>
</fieldset>
```
Legend text is announced with every control inside, so keep it short. A visible group heading without `fieldset` or `role="group"` plus `aria-labelledby` leaves the group unnamed. A single checkbox does not need a fieldset.

## Autocomplete (1.3.5, AA)

Fields collecting information about the user must expose their purpose using the HTML `autocomplete` attribute with valid tokens.
`name`, `given-name`, `family-name`, `email`, `tel`, `username`, `current-password`, `new-password`, `street-address`, `address-line1`, `address-level2` (city), `address-level1` (state), `postal-code`, `country`, `bday`, `organization`, `cc-name`, `cc-number`, `cc-exp`, `cc-csc`, `one-time-code`.
- Wrong or invented tokens (`autocomplete="off"` on a login field, `autocomplete="fname"`) count as failures or defeat password managers.
- Do not set `autocomplete="off"` on login or identity fields; it works against 3.3.8 and 3.3.7.

## Error identification (3.3.1, A) and suggestions (3.3.3, AA)

When an error is detected automatically, identify the field and describe the error in text. When a fix is known, suggest it, unless that would compromise security or purpose.
- Text message adjacent to the field, naming the problem and the fix: "Enter a date as DD/MM/YYYY", not "Invalid input".
- Programmatic link: `aria-invalid="true"` on the input and the message in `aria-describedby`. Set `aria-invalid` only after validation fails, not on first render.
- Do not rely on color, a red border, or an icon alone (1.4.1).
- Validation timing: avoid validating on every keystroke or on first blur with a distracting alert. Validate on blur or submit, and clear the error as soon as the value becomes valid.
- Prefer native constraint validation attributes (`required`, `type`, `pattern`, `minlength`) as the baseline, but replace default bubble UI with your own messages if the bubbles are not reliably announced; if using `noValidate`, you own every message.

### On submit with errors

Pattern that works across screen readers:
1. Render an error summary at the top of the form: `<div role="alert" tabIndex={-1} ref={summaryRef}>` containing "There are 2 problems" and a list of links to each field (`<a href="#email">Email: enter a valid address</a>`).
2. Move focus to the summary (or to the first invalid field if there is one error) after render.
3. Keep inline messages next to each field.
Do not only toast the error and leave focus on the submit button. Do not clear user input on error.
Server errors (409, 500) get the same treatment plus a retry path; keep the form data.

## Error prevention (3.3.4, AA)

For pages that cause legal commitments or financial transactions, modify or delete user-controllable data, or submit test responses, provide at least one of: reversible, checked with chance to correct, or confirmed before final submission. Concretely: a review step before payment, an undo window with a visible "Undo" control that is keyboard reachable and lasts long enough, or a confirm dialog for destructive deletes. A toast with Undo that vanishes in 3 seconds is not a reliable mechanism (see 2.2.1 in `target-size-and-motion.md`).

## Redundant entry (3.3.7, A, new in 2.2)

Information the user already entered in the same process must be auto-populated or selectable, not requested again, except when re-entry is essential (confirming a new password), for security, or when the earlier data is no longer valid. Check multi-step checkouts for repeated billing/shipping addresses ("same as shipping" checkbox is a pass), repeated emails, and wizards that lose values on Back. Persist step state across steps.

## Accessible authentication (3.3.8, AA, new in 2.2)

A login step must not require a cognitive function test (remembering a password, solving a puzzle, transcribing characters) unless an alternative or assistance exists. Pass if the process supports:
- Password managers and autofill: correct `autocomplete="username"`, `current-password`, `new-password`; no blocked paste; fields not split or masked in ways that break filling.
- Copy-paste into the field, passkeys/WebAuthn, email link, or SMS/authenticator code that can be pasted or autofilled (`autocomplete="one-time-code"`).
- Exception: object recognition (select pictures of cats) and recognizing user-provided content are allowed at AA, but any "type the characters", "solve this puzzle", or "rearrange items" CAPTCHA with no alternative fails.
Flag: paste handlers calling `preventDefault`, OTP inputs that are six separate boxes with no paste/auto-advance support, CAPTCHA with no alternative.

## Consistent help (3.2.6, A, new in 2.2)

If a help mechanism (contact link, chat, FAQ link) appears on multiple pages, it must be in the same relative place across them.

## Status messages (4.1.3, AA)

Status messages that appear without moving focus must be exposed to assistive technology through roles or properties: "Saved", "3 results found", "Item added to cart", "Loading", validation counts.

| Case | Use | Notes |
|---|---|---|
| Successful save, result counts, progress, cart updates | `role="status"` (polite, atomic) | Waits for the user to finish speaking |
| Error that blocks the task, session about to expire | `role="alert"` (assertive) | Interrupts; use sparingly |
| Persistent visible message the user will encounter by reading | Neither; ordinary text | Do not announce what the user is already focused on |
| Long, interactive toasts with buttons | Neither alone; move focus or keep them reachable | Live regions cannot be navigated into reliably |

Implementation rules (React):
- The live region container must already exist in the DOM before its text changes. Mounting `<div role="status">Saved</div>` with its content in one render is often not announced.
```tsx
<div role="status" aria-live="polite" className="sr-only">{message}</div>  // always rendered; message state changes
```
- Keep it in the layout once (a single announcer) rather than one per toast.
- `aria-atomic="true"` when the whole message must be re-read; `role="status"` and `role="alert"` already imply it.
- Do not hide the region with `display: none` or `aria-hidden`; use the `sr-only` clip technique.
- Clear or replace the message so identical consecutive messages re-announce (append a changing character or clear first).
- Do not put `aria-live` on a large container (a whole results list) that updates frequently; announce a short summary ("12 results") instead.
- Do not use `alert` for success messages.
- Whether a message is actually spoken, and its timing, must be verified with VoiceOver; mark NEEDS-TEST.

## Loading and async updates

- A control that triggers async work shows a busy state in text, not only a spinner: "Saving..." in a status region. Set `aria-busy="true"` on a region being updated only if the update is atomic; do not leave it set.
- Spinner icons are `aria-hidden`; the word carries the meaning.
- Prevent double submit by disabling after submit, but keep focus: if the focused submit button becomes `disabled`, focus is lost in some browsers. Use `aria-disabled="true"` and ignore clicks, or move focus deliberately.
- Skeletons and lazy lists: when content replaces a loader, announce completion ("Results loaded") and do not move focus unprompted. Infinite scroll needs a keyboard-reachable "Load more" or equivalent, and the footer must stay reachable.
- Optimistic updates that roll back must announce the rollback as an alert.
- Timeouts, expiring sessions, and autosave: see 2.2.1 in `target-size-and-motion.md`.
