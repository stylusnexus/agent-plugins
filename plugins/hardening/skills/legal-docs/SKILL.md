---
name: legal-docs
description: Draft or review the customer-facing legal documents of a small SaaS - Terms of Service, Privacy Policy, refund policy, and acceptable use policy - in plain English, with placeholders instead of invented facts, a check that every claim matches what the product actually does, and a not-legal-advice notice on every draft. Use when asked to "write terms", "draft a privacy policy", "update our ToS", "write a refund policy", or before launching a product or feature that changes what data is collected or how billing works.
---

# Legal Docs

> **Not legal advice.** This skill produces drafts and review notes, not legal advice, and it is not a substitute for a lawyer. Laws differ by country and state and change over time. Have a qualified lawyer in the relevant jurisdictions review every document before it is published or relied on.

## Overview

A method for drafting and reviewing the four documents a small SaaS usually needs, so they are readable, specific to the product, and do not claim more than the product does. Generic templates miss what is particular to a product: what it collects, who processes it, how billing and refunds really work, what users may not do. The most dangerous error in these documents is not bad wording. It is a confident statement about the product that is false.

If the repository defines its own `legal-docs` skill, follow that one instead.

## Workflow

1. **Map the product's legal surface from evidence, before drafting anything.** For each item, note where the answer came from (code, configuration, a vendor contract, the owner):
   - **Data:** what personal data is collected, where it is stored, how long it is kept, and who can reach it. Use the `privacy-audit` skill's inventory if one exists; do not re-derive it from the existing policy.
   - **Processors:** every third party that receives user data (payments, analytics, email, error tracking, hosting, model APIs). Each one publishes a data processing agreement and a subprocessor list, for example [Stripe's DPA](https://stripe.com/legal/dpa) and [PostHog's DPA](https://posthog.com/dpa). Link them; do not paraphrase their terms from memory.
   - **Money:** plans, trials, renewal, cancellation timing, proration, and what the billing provider actually does on each.
   - **Content:** who owns what users create, what license the service needs to host and display it, and any third-party content or licenses the product ships.
   - **Product-specific risks:** AI-generated output (disclose it and say it can be wrong), user-supplied credentials such as API keys (how they are stored, what happens on account deletion, who pays the third party), integrations that act on the user's behalf.

2. **Decide which documents are needed, and keep them separate.** They answer different questions for different readers at different times:
   - **Terms of Service:** acceptance, accounts, acceptable use (or a link to the AUP), ownership of user content and the license granted to the service, billing and refunds (or a link to the refund policy), termination, disclaimers and limitation of liability, changes to the terms, governing law.
   - **Privacy Policy:** what is collected and why, the legal basis where required, processors, retention, international transfers, user rights and how to exercise them, cookies and tracking, contact for privacy requests.
   - **Refund policy:** trial terms, what "no refund after trial" or "prorated refund" means in practice, cancellation timing for monthly and annual plans, explicit non-refund conditions.
   - **Acceptable use policy:** what users may not do (abuse, illegal content, scraping, reselling, attacking the service), and what the service may do about it.

3. **Identify which laws plausibly apply, and say so as a question for the lawyer, not a conclusion.** Examples of what to raise, with the primary source:
   - **EU users:** the GDPR applies to processing of personal data of people in the EU in some circumstances even when the business is outside the EU (Article 3). Article 13 lists what a privacy notice must tell people when data is collected from them; Articles 15 to 22 set out their rights (access, rectification, erasure, restriction, portability, objection, and rights around automated decisions). Source: [Regulation (EU) 2016/679](https://eur-lex.europa.eu/eli/reg/2016/679/oj). UK users are covered by the UK's own data protection law, a separate question for the lawyer.
   - **California residents:** the CCPA gives consumers rights to know, delete, correct, opt out of sale or sharing, and limit use of sensitive personal information, and it applies only to businesses that meet its thresholds. Read the current thresholds and rights on the [California Attorney General's CCPA page](https://oag.ca.gov/privacy/ccpa) and the [California Privacy Protection Agency's regulations](https://cppa.ca.gov/regulations/); do not assume they apply or do not.
   - **Consumer refunds:** consumer-protection law can give buyers rights a refund policy cannot remove. For example, the EU Consumer Rights Directive gives a 14-day right of withdrawal for distance contracts (Article 9), with exceptions listed in Article 16; whether any exception covers a subscription service is a question for the lawyer. Source: [Directive 2011/83/EU](https://eur-lex.europa.eu/eli/dir/2011/83/oj).
   - Anything else (children's data, health or financial data, a specific industry, a specific country) is a question for the lawyer. Write it down; do not draft around it.

4. **Draft in plain English.** Short sentences, active voice, and headings a customer would search for ("Can I get a refund?", not "Section 7(b): Remuneration Reversal"). No "heretofore", no "party of the first part".

5. **Use placeholders for facts you do not have.** `[COMPANY_LEGAL_NAME]`, `[COMPANY_ADDRESS]`, `[GOVERNING_LAW]`, `[DISPUTE_VENUE]`, `[PRIVACY_CONTACT_EMAIL]`, `[RETENTION_PERIOD_FOR_X]`. Mark each for the owner to fill in. Never guess a jurisdiction, an entity type, or a retention period.

6. **Review for overclaiming.** Check every factual sentence against the evidence from step 1. Watch for:
   - Compliance claims ("we are GDPR compliant", "fully secure", "bank-level encryption"). Replace them with what the product actually does ("passwords are hashed; data is encrypted in transit and at rest by our hosting provider") and only if step 1 confirmed it.
   - Absolute promises ("we never share your data") that a processor list contradicts.
   - Processors used in code but missing from the policy, or listed in the policy but no longer used.
   - Rights the policy offers that the product cannot fulfil (an export or deletion flow that does not exist).
   - Refund terms that contradict the pricing page, a migration promise, or what the billing setup really does. A `pricing-review` skill, if installed, holds any grandfathering promises.

7. **Put the notice on every draft.** At the top and bottom of each document:
   > *Draft for review. This is not legal advice and has not been reviewed by a lawyer. Have it reviewed by qualified legal counsel in the relevant jurisdictions before publishing or relying on it.*

## Worked example

Request: "Write a privacy policy for our scheduling app before launch."

1. **Surface, from evidence:** the code collects name, email, calendar event titles and times, and IP address in logs. Processors found in code and configuration: Stripe (payments), PostHog (analytics), an email provider, Sentry (errors), the hosting provider. Logs are kept for 30 days (from the log host's configuration). There is an account-deletion flow but no data export.
2. **Documents:** Privacy Policy now; the existing Terms already link a refund policy.
3. **Applicable law, as questions:** the app accepts EU signups, so the GDPR questions (legal basis, Article 13 contents, rights handling) go on the lawyer's list. Whether the CCPA applies depends on thresholds the owner must check.
4. **Draft:** plain-English sections: "What we collect", "Why", "Who we share it with" (each processor linked to its DPA), "How long we keep it", "Your choices and rights", "Cookies and analytics", "Contact us".
5. **Placeholders:** `[COMPANY_LEGAL_NAME]`, `[PRIVACY_CONTACT_EMAIL]`, `[RETENTION_PERIOD_FOR_ACCOUNT_DATA]`.
6. **Overclaiming caught:** the requester's notes say "users can download all their data"; no export flow exists, so the draft says "contact us to request a copy" and the gap is reported. "We never sell your data" is kept only after confirming that no processor receives data for advertising.
7. **Notice:** added at top and bottom. The draft goes to the owner and lawyer, not to the live site.

## Checklist

- [ ] Legal surface mapped from code, configuration, and contracts, with a source for each item
- [ ] Each document drafted separately; only the ones needed
- [ ] Applicable-law questions listed with primary sources, not answered as conclusions
- [ ] Plain-English pass done
- [ ] Unknown facts left as marked placeholders
- [ ] Every factual sentence checked against evidence; no compliance or absolute claims without support
- [ ] Not-legal-advice notice at the top and bottom of every draft

## Output

The requested drafts (or one revised section for an update) as Markdown, plus a short list of open questions for the lawyer and gaps found between the documents and the product. Keep drafts out of the live site until a lawyer has reviewed them.

## Stop conditions

- Asked to present a draft as final, lawyer-reviewed, or legally binding: refuse. The notice stays however the request is phrased.
- Asked to state compliance with a law without evidence that the practices support it: do not assert it. Describe what the product does and report the gap (the `privacy-audit` skill checks the practices).
- The jurisdiction, entity type, or audience (for example, whether children use the product) is unclear and would change the document: ask rather than guess.
