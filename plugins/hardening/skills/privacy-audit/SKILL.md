---
name: privacy-audit
description: Data inventory and privacy audit for a product — enumerate exactly what user data is collected and where it lands (Neon/Supabase tables, logs, PostHog, Stripe, email provider, Better Stack/Sentry), check alignment with the privacy policy, verify GDPR export/delete paths exist, and grep for PII leaking into logs or API responses. Use when asked to "audit privacy," "check what data we collect," before a launch, or after adding a new data-collecting feature (signup field, analytics event, webhook).
---

# Privacy Audit

## Overview
The rule is explicit: **a privacy policy is required if any user data is collected, and the team must know exactly where it's stored.** This skill produces that inventory and checks it against reality — not against what the privacy policy claims, but against what the code and infra actually do. Apply it first to anything public-facing that collects user data. Internal or proprietary services need the same discipline whenever they touch partner or customer data, even where no public policy is required.

## Workflow

1. **Enumerate data collection points.** Grep the codebase for the shape of intake, not just obvious forms:
   - Signup/auth forms (NextAuth v5 — check `providers` config and any custom `signIn`/`session` callbacks for extra fields captured).
   - Any Zod schema in a route handler with fields beyond `id`/`createdAt` — `grep -rn "z.object" --include="*.ts"` and read what each schema captures.
   - Stripe customer/subscription metadata (`stripe.customers.create`, `metadata:` blocks) — Stripe stores whatever you attach.
   - PostHog `capture()`/`identify()` calls — check `properties:` payloads for anything beyond anonymous event data (email, name, IP if not stripped).
   - File uploads (campaign assets, avatars) — where do they land (S3/R2/local disk) and is there EXIF/metadata scrubbing?
   - BYOK products: the user's own Anthropic/OpenAI API key — this is the most sensitive field in the product. Confirm it is encrypted at rest, never logged, and never returned in any API response after initial save.

2. **Build the data map.** For every field found, record: field name → source (which form/event) → storage location (table.column, PostHog event property, Stripe metadata key, log line) → retention (indefinite / N days / until account deletion) → who else sees it (third-party processor: Stripe, PostHog, email provider, Sentry/Better Stack).
   - Table format works well here — one row per data category (email, name, BYOK key, IP, campaign content, payment method) with those five columns.

3. **Check privacy-policy alignment.** Read the live privacy policy (or draft from `legal-docs` skill if none exists) and confirm every row in the data map is disclosed. Flag:
   - Data collected but not mentioned in the policy (the common miss: PostHog session recordings, IP addresses in logs, third-party sub-processors not listed).
   - Policy claims that aren't true anymore (e.g., "we do not use analytics" when PostHog was added later).

4. **Verify GDPR basics exist** — even for a small SaaS, these two paths matter if any EU users are plausible:
   - **Export:** is there a way (self-serve or manual) for a user to get all their data? Check for a `/api/account/export` route or equivalent; if none, note it as a gap.
   - **Delete:** does account deletion actually cascade — Prisma `onDelete: Cascade` on user-owned tables, Stripe customer deletion/anonymization, PostHog `person` deletion via API, removal from email provider list. A "delete" that leaves orphaned rows or a still-subscribed Stripe customer is not a real delete path.

5. **Run grep-based PII leak scans** against logs and API responses:
   - Logs: `grep -rn "console.log\|logger\." --include="*.ts" -A2 | grep -iE "email|password|apiKey|token|ssn|address"` — anything printing a raw user object is a likely leak (`console.log(user)` instead of `console.log(user.id)`).
   - API responses: for each route handler, check the response payload against the Prisma model — is `select`/`omit` used to exclude `passwordHash`, `apiKeyEncrypted`, internal `stripeCustomerId` unless the client legitimately needs it? A bare `return NextResponse.json(user)` without a `select` clause is the classic over-fetch leak.
   - Error responses: confirm error handlers don't stringify raw exceptions containing env vars or connection strings back to the client (`error.message` from a Postgres connection failure can leak a DB host).
   - Sentry/Better Stack: check `beforeSend`/scrubbing config — is PII scrubbing configured, or does every error event ship the full request body?

6. **Report format:** data map table, policy-alignment gaps (list), GDPR path status (exists / partial / missing, per path), PII leak scan findings (file:line + what's exposed), and a prioritized fix list (leaks first, then policy gaps, then GDPR paths).

## Checklist
- [ ] Every data collection point enumerated (forms, Zod schemas, Stripe metadata, PostHog events, file uploads, BYOK keys)
- [ ] Data map built: field → source → storage → retention → third parties
- [ ] Privacy policy checked line-by-line against the data map
- [ ] Export path verified (or flagged missing)
- [ ] Delete path verified end-to-end, including third-party cascade (Stripe, PostHog, email list)
- [ ] Log grep run for PII patterns
- [ ] API response grep run for over-fetch (`select`/`omit` missing on sensitive fields)
- [ ] BYOK key handling verified (encrypted at rest, never logged, never returned) — BYOK products only

## Output
A data-map table plus a findings list with file:line references for every leak found. Do not write this to a persistent `.md` file unless asked — return it in the response.

## Stop Conditions
- A PII leak is found in a **production** log stream or a live API response → report it immediately as the top finding, don't bury it under lower-priority items; this may need an urgent fix and log scrubbing/rotation, not just a backlog ticket.
- The audit surfaces a legal gap (no GDPR delete path, undisclosed data collection, BYOK keys stored in plaintext) → do not attempt to unilaterally draft policy language or push a schema migration to "fix" it; flag it and hand off to `legal-docs` (for policy text) or a scoped implementation task with the user's sign-off (for the encryption/migration fix), since these touch production data.
- Any finding requires reading a recovery-code file or similar secret to verify → stop and confirm with the user first.
