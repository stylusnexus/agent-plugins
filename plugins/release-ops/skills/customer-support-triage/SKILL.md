---
name: customer-support-triage
description: Support inbox workflow for a small team - classify each request (bug, feature request, billing, how-to), attempt reproduction, assign severity, file a standard GitHub issue with no customer PII, check refund requests against the written policy, and draft the reply for a human to send. Use when triaging support email or tickets, or when asked to "handle this support request", "file this bug", or "draft a reply to this customer".
---

# Customer Support Triage

## Overview

A repeatable path from "a customer message arrived" to "issue filed, reply drafted, nothing dropped". A small team has no dedicated support staff, so every ticket needs a fast, consistent path or it turns into customer debt.

If the repository defines its own `customer-support-triage` skill, follow that one instead. Tool names below (Sentry, Better Stack, Stripe) are examples; use the error tracker, log host, and billing provider the project actually has.

This skill files GitHub issues in the project's own repository and drafts everything else. It never sends a reply, issues a refund without a person's confirmation, or posts anywhere outside the repository.

## Workflow

1. **Classify the request** into exactly one primary category (secondary tags allowed):
   - **Bug:** something that should work and does not.
   - **Feature request:** something that does not exist and is being asked for.
   - **Billing:** subscription, invoice, refund, upgrade or downgrade, failed payment.
   - **How-to:** the feature exists and the customer has not found it.
   - The most common misclassification is a "bug" that is really a how-to: "it's broken" because a feature is opt-in and not enabled. Verify before filing.
   - If customers bring their own model API keys, questions about model charges are between them and their provider. Billing tickets then concern only your own subscription.

2. **Attempt reproduction (bugs only).** Before filing anything:
   - Check the customer's plan and any feature flags that apply to them. Many "bugs" are a flag that is off for their cohort; a `feature-flags` skill, if installed, covers flag state.
   - Reproduce locally or in staging with the inputs the customer described. If it reproduces, write down the exact steps. If not, record what was tried and label the issue "needs more info" instead of filing a vague bug.
   - Search the error tracker and logs around the reported time. A stack trace beats a guess.

3. **Assign severity, with a stated reason:**
   - **P0 (critical):** data loss, security exposure, double charge, product-wide outage. Do not wait for the normal triage cadence. A live outage goes to the `incident-response` skill.
   - **P1 (high):** a feature is broken for a group of users, with no workaround.
   - **P2 (medium):** broken with a workaround, or a narrow edge case.
   - **P3 (low):** cosmetic, a minor annoyance, or a feature request.
   - An actual overcharge or a failed refund is P0 or P1 regardless of technical severity. Money problems move fast.

4. **File the GitHub issue** (bugs and feature requests). If the user asked for drafts only, return the issue text instead of filing it. Use the repository's issue template if it has one (`.github/ISSUE_TEMPLATE/`); otherwise this one:
   ```
   ## Summary
   [one line]

   ## Reported by
   [ticket ID or link. No email, name, or other PII.]

   ## Severity
   P0/P1/P2/P3 - [reason]

   ## Repro steps
   1. ...
   2. ...

   ## Expected vs actual
   Expected: ...
   Actual: ...

   ## Environment
   Plan: ... / Browser: ... / Flag state: ...

   ## Notes
   [error-tracker link, related issues, workaround if any]
   ```
   Use the repository's existing labels (`gh label list`) for type and severity; do not invent new ones. Never paste the customer's raw message, email address, or other PII into the issue. Issues usually have wider read access than the support inbox; reference the ticket ID instead.

5. **Check refund requests against the written policy:**
   - Read the product's published refund policy (trial terms, proration, non-refund conditions). A `legal-docs` skill, if installed, drafts that policy.
   - Inside the policy: prepare the refund (amount, charge, reason) for a person to confirm. Issue it only after that person confirms, in the billing provider (for Stripe, from the Dashboard or the Refunds API; see [Stripe, Refunds](https://docs.stripe.com/refunds)).
   - Outside the policy (past the window, a goodwill request, a repeat refunder): do not decide. Flag it for the person who owns refund decisions. Refunds are real money leaving the business.

6. **Draft the customer reply.** Match tone to the category: how-to replies are short and warm; bug replies acknowledge the problem and set expectations without promising a fix date; billing replies are exact about amounts and dates.
   - If the reply goes out under a named person's signature, that person edits it before it is sent. The `human-writing` skill (in the `reporting-comms` pack), if installed, helps it read like a person wrote it.
   - An unsigned system reply (an automatic acknowledgement from a no-reply address) needs only plain, clear copy.

## Worked example

Ticket #4812: "Export to PDF is broken. I click the button and nothing happens. I'm on the annual plan."

1. **Classify:** reported as a bug. Checking the plan shows PDF export is enabled for annual plans behind the `export-pdf-v2` flag, and the flag is on for this account, so it is not a how-to.
2. **Reproduce:** staging with the same plan and a 40-page document reproduces it. The error tracker shows `PayloadTooLargeError` from the export endpoint at the reported time; documents over 30 pages fail.
3. **Severity:** P1. Export is broken for every customer with long documents, and there is no workaround.
4. **Issue:** filed with the template, "Reported by: ticket #4812", repro steps, the error-tracker link, and the repository's `bug` and `priority: high` labels. No customer email in the body.
5. **Refund:** none requested.
6. **Reply draft (marked DRAFT, for the support owner to send):** "Thanks for reporting this. We can reproduce it: PDF export fails for documents over about 30 pages. We've logged it as a high-priority bug. Until it's fixed, exporting in sections works. We'll write back when the fix is live."

## Checklist

- [ ] Classified correctly (bug versus how-to is the most common miss)
- [ ] Reproduction attempted for bugs, cross-checked against error tracker and logs
- [ ] Severity assigned with a stated reason
- [ ] GitHub issue filed with the template and existing labels, no PII in the body
- [ ] Refund checked against the written policy; anything outside it flagged, not decided
- [ ] Reply drafted and marked as a draft; a named sender reviews it before it goes out

## Output

A triage summary (category, severity, issue link) plus the drafted reply, clearly marked as a draft pending send.

## Stop conditions

- P0 severity (data loss, security exposure, double charge): put it on the first line of the response, not inside a normal summary.
- A refund request falls outside the written policy: do not process it; flag it for the decision owner.
- Reproduction would need access to the customer's account data beyond what the ticket contains (impersonating their session, reading their database rows): do not do it without explicit authorization. Work from the ticket and a staging reproduction.
