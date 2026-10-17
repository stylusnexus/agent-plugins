---
name: webhook-reliability
description: Design or review inbound and outbound webhooks for signature verification, idempotency, retry/backoff, dead-letter recording, replay tooling, and timeout budgets. Use when building a new webhook handler or emitter, reviewing an existing one (Stripe, GitHub, or a custom outbound webhook), or investigating a "webhook silently didn't fire" report.
---

# Webhook Reliability

## Overview

Webhooks fail silently by nature — there's no user staring at a spinner when one drops, so the failure mode is "data quietly went stale" discovered days later. This skill covers both directions: **inbound** (Stripe, GitHub sending events to us) and **outbound** (if your product emits webhooks to third parties or customers). The core disciplines — verify, dedupe, retry, record dead letters, monitor — apply to both.

## Inbound webhooks

1. **Signature verification is mandatory, always, first line of the handler** — never process a payload before verifying it came from the claimed sender:
   ```ts
   // Read the raw body once, before any parsing — req.json() first means the bytes no longer match the signature
   const rawBody = await req.text();

   // Stripe
   const event = stripe.webhooks.constructEvent(rawBody, req.headers.get('stripe-signature')!, process.env.STRIPE_WEBHOOK_SECRET!);

   // GitHub
   import { createHmac, timingSafeEqual } from 'crypto';
   const sig = Buffer.from(req.headers.get('x-hub-signature-256') ?? '');
   const expected = Buffer.from('sha256=' + createHmac('sha256', process.env.GITHUB_WEBHOOK_SECRET!).update(rawBody).digest('hex'));
   if (sig.length !== expected.length || !timingSafeEqual(sig, expected)) {
     return new Response('Invalid signature', { status: 401 });
   }
   ```
   Use `timingSafeEqual`, never `===`, for signature comparison — a naive string comparison leaks timing information. `timingSafeEqual` throws a `RangeError` (`ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH`) when the buffers differ in length, so check lengths first or a malformed header turns into a 500 instead of a 401.

2. **Idempotency** — providers can deliver the same event more than once (Stripe retries; a GitHub redelivery reuses the original id). Record the provider's event id in a table with a unique constraint — Stripe's `event.id`, or GitHub's `X-GitHub-Delivery` header, which "will be the same as in the original delivery" on a redelivery ([GitHub: best practices for using webhooks](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks)):
   ```prisma
   model WebhookEvent {
     id         String   @id @default(cuid())
     provider   String   // "stripe" | "github"
     externalId String   // event.id from the provider
     receivedAt DateTime @default(now())
     @@unique([provider, externalId])
   }
   ```
   ```ts
   try {
     await prisma.$transaction(async (tx) => {
       await tx.webhookEvent.create({ data: { provider: 'stripe', externalId: event.id } });
       await applyEvent(tx, event); // or enqueue the job inside the same transaction
     });
   } catch (e) {
     if (isUniqueConstraintError(e)) return new Response('Already processed', { status: 200 });
     throw e; // non-2xx, so the provider can retry
   }
   ```
   Write the idempotency record only together with successful processing (same transaction), or after it — never before. If the id is committed first and the handler then fails, the retry looks like a duplicate, gets skipped, and the event is lost.

3. **Timeout budget** — providers expect a fast ack (Stripe: respond within a few seconds or it's treated as a failed delivery and retried; GitHub: respond with a 2xx within 10 seconds or the delivery is marked failed). Do the minimal synchronous work (verify + record + enqueue), push anything slow (sending a welcome email, recomputing analytics) to a background job rather than doing it inline before responding.

4. **Return the right status code** — 2xx only after the event is durably recorded (not necessarily fully processed if processing is async). Any failure to verify/record should return non-2xx so the provider retries — swallowing an error and returning 200 anyway is the single most common cause of silent data loss.

5. **Know who retries** — Stripe retries failed live-mode deliveries for up to 3 days. GitHub does **not**: "GitHub does not automatically redeliver failed webhook deliveries" ([GitHub: handling failed webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/handling-failed-webhook-deliveries)). Redeliver from the UI or REST API, or run a scheduled job that lists failed deliveries and redelivers them. Check each provider's policy before relying on its retries.

6. **Dead-letter recording** — providers don't write dead letters for you. When your own background processing exhausts its retries, your job writes a durable record, not just a log line that scrolls away:
   ```prisma
   model WebhookDeadLetter {
     id         String   @id @default(cuid())
     provider   String
     externalId String
     payload    Json
     lastError  String
     failedAt   DateTime @default(now())
   }
   ```
   Alert on any row appearing here (Better Stack log-based alert on the "dead letter recorded" log line, or a simple daily count check) — a dead letter with no one looking at it is worse than no dead-letter table at all, because it creates false confidence.

7. **Replay tooling** — a small internal script or admin route to re-fetch a stored dead-letter payload and re-run it through the same handler logic, so recovering from a bug doesn't require asking the provider to manually resend:
   ```ts
   // scripts/replay-webhook.ts
   const dl = await prisma.webhookDeadLetter.findUniqueOrThrow({ where: { id: deadLetterId } });
   await processStripeEvent(dl.payload as Stripe.Event); // same function the live handler calls
   await prisma.webhookDeadLetter.delete({ where: { id: deadLetterId } });
   ```

## Outbound webhooks (if the product emits any)

1. **Retry with exponential backoff and jitter** — 3–5 attempts, backoff like 1m/5m/30m/2h, capped, then dead-letter. Following the [Standard Webhooks spec](https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md): only a 2xx is success; retry timeouts, connection errors, and other non-2xx responses (redirects count as failures — don't follow them); on `429`, `502`, or `504`, slow down and honor any `Retry-After`; on `410 Gone`, stop and disable the endpoint.
2. **Sign outgoing payloads** with HMAC-SHA256 and a per-customer secret, and include a timestamp in both the signed content and a header (Standard Webhooks signs `msg_id.timestamp.payload`) so receivers can reject stale replays by checking the timestamp is within a tolerance.
3. **Idempotency key on outbound sends** — include an event id in the payload so receivers can dedupe on their end too; this is a courtesy that also protects them from your own retries.
4. **Timeout the outbound HTTP call itself** (e.g., 10s) — don't let a slow/hanging receiver block the sending worker indefinitely.

## Monitoring for silent failures

- Alert (Better Stack) on: webhook endpoint 5xx rate, dead-letter table row count > 0, and a gap in expected event volume (e.g., zero Stripe events received in an hour when there's normally steady traffic — could mean the endpoint URL is misconfigured in the Stripe dashboard, not that the app is broken).
- Log every received event id and outcome (processed / duplicate / dead-lettered) at INFO level for traceability, scrubbed of PII/payment details per the logging house rule.

## Output / Evidence

Show the user: the signature verification code path, the idempotency table/constraint, a captured example of a duplicate delivery being correctly skipped (log line or test), and the dead-letter table schema plus how it's monitored. For an audit of an existing webhook, report which of the above are present vs missing per handler.

## Stop Conditions

- A webhook handler processes the payload before verifying the signature — stop, this is a critical fix, not a nice-to-have, treat as a security bug.
- No idempotency mechanism and the handler has side effects that aren't naturally idempotent (e.g., sends an email, increments a counter) — stop and flag the risk of duplicate side effects before shipping.
- Dead-letter table exists but nothing monitors it — note this as incomplete; a silent dead-letter table gives false confidence and should be called out explicitly, not treated as "done."
