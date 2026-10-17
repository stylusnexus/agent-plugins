---
name: rate-limit-audit
description: Pre-launch gate that inventories every endpoint calling a paid API (LLM, email, SMS) and every auth endpoint, verifies a rate limiter exists, and actually tests it with scripted burst requests to confirm 429s fire. Use before launching a new product/feature, after adding an LLM-calling or auth route, or when asked to check rate limiting.
---

# Rate Limit Audit

## Overview

A rate limiter that's configured but never tested is a rate limiter that might not actually work — wrong key extraction, wrong window, or a middleware ordering bug can all silently no-op it. This skill's job is proving the limit fires, not just confirming code that looks like a limiter exists. Required pre-launch on any endpoint that calls a paid API (Anthropic/Vercel AI SDK, email, SMS) and on all auth endpoints (login, password reset, OTP, signup) — per the house security rules.

## Workflow

1. **Inventory every endpoint in scope** — grep the App Router for candidates:
   ```bash
   # Paid-API-calling routes
   grep -rl "anthropic\|generateText\|streamText\|@ai-sdk" app/api
   grep -rl "sendEmail\|resend\|sendgrid\|nodemailer" app/api
   grep -rl "twilio\|sendSms" app/api

   # Auth-adjacent routes
   grep -rl "signIn\|signUp\|reset-password\|verify-otp\|magic-link" app/api
   ```
   Also search files marked `'use server'` — server actions call paid APIs and run auth flows too, and they're reachable by a direct POST, so they need the same limiter as the route handlers. Build a table: route path or server action, category (LLM / email / SMS / auth), current limiter (none / found), limiter library used.

2. **Recommend defaults per endpoint class** (starting points — tune to actual cost/abuse profile):

   | Class | Suggested limit | Key |
   |---|---|---|
   | LLM chat/completion endpoint | 20 req / 10 min per user | user id (fallback IP if anonymous) |
   | LLM endpoint, anonymous/free tier | 5 req / 10 min | IP |
   | Email send (transactional) | 10 / hour per recipient | recipient email + IP |
   | Email send (bulk/invite) | 5 / hour per sender | user id |
   | SMS/OTP send | 3 / 10 min, 10 / day | phone number |
   | Login attempt | 5 / 15 min | IP + email combo (lock the pair, not just the IP) |
   | Password reset request | 3 / hour | email (return same response regardless of match) |
   | Signup | 10 / hour | IP |

3. **Verify implementation** — for Next.js on Render (no built-in edge rate-limit infra like Vercel's), the common pattern is a Postgres- or Redis-backed limiter. The check and the increment must be one atomic statement — a count-then-insert lets concurrent requests all read the same count and all pass:
   ```ts
   // lib/rate-limit.ts — fixed window over Postgres, one atomic upsert, no extra infra needed
   // table: rate_limit(key text, window_start bigint, count int, primary key (key, window_start))
   export async function checkRateLimit(key: string, limit: number, windowSeconds: number) {
     const now = Math.floor(Date.now() / 1000);
     const windowStart = now - (now % windowSeconds);
     const [{ count }] = await prisma.$queryRaw<{ count: number }[]>`
       INSERT INTO rate_limit (key, window_start, count) VALUES (${key}, ${windowStart}, 1)
       ON CONFLICT (key, window_start) DO UPDATE SET count = rate_limit.count + 1
       RETURNING count`;
     return { allowed: count <= limit, retryAfter: windowStart + windowSeconds - now };
   }
   ```
   `INSERT ... ON CONFLICT DO UPDATE` guarantees an atomic insert-or-update outcome ([PostgreSQL: INSERT](https://www.postgresql.org/docs/current/sql-insert.html)). Delete expired windows on a schedule.
   In the route handler:
   ```ts
   const { allowed, retryAfter } = await checkRateLimit(`llm:${userId}`, 20, 600);
   if (!allowed) {
     return new Response('Too many requests', { status: 429, headers: { 'Retry-After': String(retryAfter) } });
   }
   ```
   A fixed window can admit up to 2x the limit at a boundary: `limit` requests at the end of one window plus `limit` at the start of the next. Upstash lists this as the fixed window's main weakness ([Upstash Ratelimit: algorithms](https://upstash.com/docs/redis/sdks/ratelimit-ts/algorithms)); use a sliding window where that matters. If Redis (Upstash) is already in the stack for a given project, prefer it over the Postgres table for lower latency (`@upstash/ratelimit` with `Ratelimit.slidingWindow(limit, "10 m")`) — but don't add a new Redis dependency solely for rate limiting on a low-traffic route.

   **Key extraction for IP-keyed limits** — take the client IP from a header your own trusted proxy or host sets, as your host documents it, never the leftmost `X-Forwarded-For` value. The client can send its own `X-Forwarded-For`, and proxies append to it, so the leftmost entry is attacker-controlled; rotating it gives a fresh bucket on every request. MDN: security uses such as rate limiting "_must only_ use IP addresses added by a trusted proxy" ([MDN: X-Forwarded-For](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For)).

4. **Actually test it with burst requests, sequential and concurrent** — this is the non-negotiable step. Run it in bash, not zsh: `export -f` is a bash feature.
   ```bash
   #!/usr/bin/env bash
   URL=https://staging.example.com/api/chat
   send() { curl -s -o /dev/null -w "%{http_code}\n" -X POST "$URL" \
     -H "Authorization: Bearer $TEST_TOKEN" -H "Content-Type: application/json" -d '{"message":"test"}'; }
   export -f send; export URL TEST_TOKEN

   # Sequential: 25 requests in quick succession against a limit of 20/10min
   for i in $(seq 1 25); do send; done | sort | uniq -c

   # Concurrent: 25 at once, after the window resets — catches count-then-insert races
   seq 1 25 | xargs -P 25 -I{} bash -c send | sort | uniq -c
   ```
   Expected output for each run: 20 lines of `200`, 5 lines of `429`. More than 40 `200`s (2x the limit) means the limiter is not working — investigate before shipping, don't assume the code is correct because it compiles. Between 21 and 40 `200`s, rerun and check whether the run crossed a window boundary: a fixed window can admit up to 2x the limit there (see above). If a run that stays inside one window still lets more than 20 through, the limiter is broken. A sequential run alone can pass while the concurrent run shows the race.

5. **Test the auth-lockout case specifically** — brute-force a login endpoint with a wrong password 6+ times, confirm the 6th+ attempt returns 429 (or an account-lock message) rather than a normal "wrong password" 401 indistinguishable from the first attempt.

6. **Document the limits** in a short reference (README section or `docs/rate-limits.md`) so future endpoints get added consistently rather than each developer picking arbitrary numbers.

## Checklist

- [ ] Every LLM-calling route inventoried and has a limiter
- [ ] Every email/SMS-sending route inventoried and has a limiter
- [ ] Every auth route (login, signup, reset, OTP) inventoried and has a limiter
- [ ] Every server action that calls a paid API or runs an auth flow inventoried and has a limiter
- [ ] Each limiter's key includes the right dimension (user/IP/email/phone — not just IP alone for account-specific abuse)
- [ ] Client IP read from a trusted proxy's header, not the leftmost `X-Forwarded-For`
- [ ] Limiter check-and-increment is one atomic operation
- [ ] Sequential and concurrent burst tests run against at least the highest-risk endpoint (LLM chat, login) with captured 429 evidence
- [ ] `Retry-After` header present on 429 responses
- [ ] Limits documented somewhere durable, not just in code comments

## Output / Evidence

Show the user the inventory table (route / class / limiter present / tested), and the raw burst-test output (`uniq -c` counts of status codes, sequential and concurrent) for at least the two highest-risk routes. A limiter claimed without a burst-test result attached should be treated as unverified.

## Stop Conditions

- Any paid-API or auth endpoint has zero rate limiting and the task is a pre-launch gate — stop, this blocks launch, don't just note it as a finding and move on.
- Burst test shows the limiter not firing (all requests succeed past the stated limit) — stop and fix before marking the audit passed.
- Rate limit keyed only on IP for an authenticated endpoint where multiple legitimate users share an IP (office NAT, mobile carrier) — flag as likely to cause false-positive lockouts, recommend combining with user id.
