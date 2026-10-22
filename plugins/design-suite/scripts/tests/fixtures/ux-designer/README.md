# ux-designer fixtures

Six small made-up changes to a generic web app. Five each plant one findability or UX problem; `clean-copy-fix` is a harmless change that must produce no finding. Each folder holds `change.diff` (the change) and `expected.md` (first line `FINDINGS: <n>`, then the problem and severity).

## Run by hand

Do this on Claude Code and again on Codex, for each case:

1. Give the agent `change.diff` only, with the prompt "Review this change; review only, do not file". Compare its findings to `expected.md`: the planted problem found, nothing invented, and zero findings for `clean-copy-fix`.
2. Make a scratch repository first so nothing touches a real tracker: `git init` a throwaway directory, recreate the before-state of the files named in `change.diff` (each context and removed line), commit it, and `git apply` the diff. Use a throwaway remote or a local issue list there. Then give it the same diff with the prompt "file what you find". Check one issue per finding, and none for `clean-copy-fix`.
3. Run step 2 a second time. Confirm no duplicate issue is filed.

Also run each case once without screenshots to confirm the agent says what it could not verify.
