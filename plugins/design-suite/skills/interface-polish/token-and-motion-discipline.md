# Token and motion discipline

Checks for how tokens, motion and state lists are wired, so one change stays one edit. Report-only unless asked. Mark findings VERIFIED or NEEDS-TEST, and list checks not performed.

## Breakpoints and tokens

- Breakpoints reassign a few tokens declared once near the top; components read the tokens.
- Check: count media queries that put raw spacing or layout values on a component instead of reassigning a token. Recommended target: zero raw values; utility-class breakpoints that map to the system's scale are fine.

## Motion token

- Every transition duration reads a token from one declared duration set (press, small, large, exit; see `motion.md`). Under `prefers-reduced-motion: reduce`, large movement becomes a fade or an instant change, following `motion.md`; spinners and state feedback stay.
- Check: grep for hard-coded durations; flip the setting and confirm the token changed (see `motion.md` for the wider reduced-motion rules).

## Theming

- A theme reads a user-level variable with a fallback, so a user's choice is never overwritten by the global token.
- Check: grep for assignments to the global theme token outside the root; each is a finding.

## Readable token files

- Production token files hold literal, readable values. Generated scales built from chained `calc()` suit prototypes, not audits.
- Check: open the token file; a reviewer can read every value without computing it.

## Unknown names fail

- An unknown token, prop or state name must fail review, not silently do nothing (a misspelled property that is ignored looks like a working one).
- Check: take each token and state name used in the spec or code and look it up in the source list; any name not found is a finding.

## Lists come from the data

- Filter options, legends and menus derive from the data's category list.
- Check: add one fake category in a test fixture; exactly one edit should be needed. Hand-written parallel lists are findings.

## Every state handled

- For each status, a label, a colour and an icon exist.
- The fallback is loud: an unknown status shows a visible error in development and logs an event in production, never a blank or default look.
- Check: list the status values, tick the three columns, then feed an unlisted value and see what renders.
- Empty, zero and missing data each get their own display. Zero shows 0. Do not reuse one placeholder ("N/A", "undefined") for all three.

## Minimal edits

- Check: count the places that must change to rename one token or status. More than one is a finding; report the count and the files.

## Long labels

- Layouts survive double-length labels. Check: double the longest label and view at the narrowest width; nothing clips or overlaps, and the main action stays in view.
