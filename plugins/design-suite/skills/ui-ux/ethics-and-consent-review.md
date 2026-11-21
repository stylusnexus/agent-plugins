# Ethics and consent review (expert review, not legal advice)

> **Scope and limits.** This is a design-level expert review of a flow for manipulative patterns and respect for user data. It is not legal advice and not a compliance audit. It never states that a product complies with GDPR, CCPA or any other law. Legal questions go to qualified counsel and the product owner. Findings are hypotheses from inspection; none is user research.

Numbers are recommended defaults unless marked as a cited figure. Tag every finding VERIFIED (seen in the build, screenshots or a network trace) or NEEDS-TEST (inferred, needs people or tooling). Missing facts are MISSING INFORMATION.

## How to run it

1. Fix the scope: which flow (sign-up, checkout, cancel, consent, settings), which user, which platform.
2. Walk the flow once as a new user, then once as someone trying to leave or refuse. Record steps and clicks for each.
3. Run the checks below. Log each failure in the output format.
4. Say when only one pass was done; an outside walkthrough adds value.

## Money and commitment

| Rule | Check |
|---|---|
| Total cost shown before the last step | Full price with fees and delivery is visible before any account prompt and before the final screen |
| Guest checkout exists | A first-time buyer can finish without creating an account |
| Leaving is no harder than joining | Count steps to cancel or downgrade against steps to sign up; no phone-only or email-only route; offer a data export on the way out |
| Feedforward labels | The button label states the outcome ("Start paid plan", not "Continue"); recurring terms and renewal date sit beside the buy button |
| Undo over confirmation | Reversible actions complete and offer undo; confirmation dialogs are kept for the irreversible |

## Defaults and consent

| Rule | Check |
|---|---|
| Non-essential options off by default | Load a clean profile and click nothing: no optional box is ticked, and non-essential requests number zero (recommended target) |
| Cookie banner parity | Reject-all matches accept-all in size, style and click depth on the first layer; closing the banner is treated as no consent; each third party is named |
| "Analytics" that is really advertising | For each cookie in a performance group, confirm it serves only the site owner, not an ad network |
| Consent is active and granular | No pre-ticked boxes; purposes are separate; consent is not bundled into terms or a newsletter signup |
| Withdrawal costs no more than granting | Clicks to withdraw are no more than clicks to grant; the control lives in settings |
| Consent states designed | Granted, refused, withdrawn and not-yet-asked each have a visible state |
| Permissions asked in context | A camera, location or contacts prompt appears at the moment the feature is used, after a line saying why |
| Optional sensitive fields allow opt-out | Fields such as gender, health or income offer "Prefer not to say"; blank is accepted |

## Data respect

| Rule | Check |
|---|---|
| Minimisation per field | Every form field has a written purpose and a retention point; extra questions are asked later, not at sign-up |
| Self-service view and delete | A signed-in user can see what is held and delete each category (for example location apart from purchase history) without contacting support |
| Rights reachable | Access, export and delete are reachable from settings in three clicks or fewer (recommended) |
| Notifications earn their place | Each notification row names a user benefit and a frequency cap; duplicates merge; a notification that was turned off stays off |
| Plain-language terms | Short sections and a plain summary that answer cancellation, deletion, and what happens if the company is sold or closes |
| Tone | No copy blames the reader for missing a setting; no shaming opt-out text ("No, I don't want savings") |

## Governance

- Name one owner with authority to halt a release or flow. Check: is there a named person whose sign-off can block launch?
- Weighted scorecard: group items by area (data collection, storage, communication, UX, governance), mark each pass or fail with a test and an owner, weight 0 to 100, and rerun each release. Weights are the team's judgement, not a standard. Check: does every item have a pass test and an owner?

## Output format

| # | Finding | Evidence tag | Fix | Owner decision |
|---|---|---|---|---|

Finding: what the user meets, in observation terms. Evidence tag: VERIFIED, NEEDS-TEST or MISSING INFORMATION. Fix: the exact change. Owner decision: accept, reject or defer, with the named person. Rate severity on the scale in `heuristics-review.md`. Close with what was and was not reviewed, then this line: "Design-level review. Not legal advice. No compliance determination made."

## Checks not performed

- Legal review of any consent basis, notice or contract.
- Real user testing; think-aloud sessions with about five people would confirm or overturn the top findings.
- Data-flow inspection: network traces, storage, retention jobs, backups.
- Vendor and processor contracts, and what third parties do with the data they receive.
