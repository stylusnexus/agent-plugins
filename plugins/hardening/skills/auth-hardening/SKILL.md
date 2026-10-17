---
name: auth-hardening
description: NextAuth v5 security audit and hardening checklist — session/cookie config, CSRF, OAuth scopes, per-route role checks, password-reset/OTP rate limits, secret rotation, session invalidation on privilege change. Use when adding auth to a new product, auditing an existing NextAuth v5 app, or reviewing any PR that touches session/role/permission code.
---

# Auth Hardening

## Overview

NextAuth v5 (Auth.js) gets the cookie/CSRF/session-signing basics right by default — the actual gap on real projects is almost always **missing per-route authorization checks**, because middleware-level route protection feels like it covers everything and doesn't. Middleware (renamed `proxy.ts` in Next.js 16) can gate page navigation; it does not gate every API route, server action, and route handler, each of which needs its own explicit check. The Next.js docs say proxy is for optimistic checks such as redirects and "should not be used as a full session management or authorization solution" ([Next.js: Proxy](https://nextjs.org/docs/app/getting-started/proxy)), so permission checks do not belong there.

## Workflow

1. **Session strategy** — for most products, `strategy: 'jwt'` is the default and fine for stateless scaling on Render. Switch to `strategy: 'database'` (session table via Prisma adapter) only when session revocation needs to be immediate (e.g., "log this user out everywhere right now" for a compromised account) — JWT sessions can't be invalidated server-side before expiry without a denylist.

2. **Cookie flags** — keep Auth.js's cookie defaults; don't set the `cookies` or `useSecureCookies` options unless you have a specific need. With no override, the session cookie gets `httpOnly: true`, `sameSite: 'lax'`, `path: '/'`, and — when the site URL is HTTPS — `secure: true` plus the `__Secure-` name prefix (`useSecureCookies` defaults from the URL protocol; see `defaultCookies` in [Auth.js `packages/core/src/lib/utils/cookie.ts`](https://github.com/nextauthjs/next-auth/blob/main/packages/core/src/lib/utils/cookie.ts)). Behind a proxy, set `AUTH_URL` or `AUTH_TRUST_HOST` so the HTTPS detection is right. If the app does override `cookies`, confirm `httpOnly` and `secure` are never disabled in production, and that `sameSite` is `'lax'` — only `'none'` (with `secure: true` mandatory) if there's a genuine cross-site embed requirement.

3. **CSRF** — NextAuth v5 handles CSRF tokens automatically for its own sign-in/callback routes. The gap is **custom API routes that mutate state based on session** (e.g., a settings-update route) — these are protected by `SameSite` cookies plus checking `Origin`/`Referer` headers on state-changing requests if the app also accepts cross-origin requests for any reason (public API, webhooks share the route prefix). If there's no legitimate cross-origin use case, same-site cookies alone are sufficient. **Server actions** are POST-only and Next.js aborts one whose `Origin` host doesn't match the `Host` (or `X-Forwarded-Host`) header; extra hosts are allowed only through `experimental.serverActions.allowedOrigins` in `next.config` ([Next.js: serverActions](https://nextjs.org/docs/app/api-reference/config/next-config-js/serverActions)). Check that list names only domains you own, and never `'null'` — a `null` origin comes from sandbox iframes and similar privacy-sensitive contexts that can still send cookies.

4. **OAuth scopes** — request the minimum scope needed, per provider:
   ```ts
   providers: [
     GitHub({
       clientId: process.env.GITHUB_ID,
       clientSecret: process.env.GITHUB_SECRET,
       authorization: { params: { scope: 'read:user user:email' } }, // not 'repo', not 'admin:org'
     }),
   ]
   ```
   Audit every configured provider's scope string against what the app actually uses — scope creep (requesting `repo` when only email is needed) is a common finding.

5. **Role checks on every protected route handler** — this is the core of the audit, not middleware:
   ```ts
   // app/api/campaigns/[id]/route.ts
   export async function DELETE(req: Request, { params }: { params: Promise<{ id: string }> }) {
     const session = await auth();
     if (!session?.user) return new Response('Unauthorized', { status: 401 });

     const { id } = await params; // params is a Promise since Next.js 15
     const campaign = await prisma.campaign.findUnique({ where: { id } });
     if (!campaign) return new Response('Not found', { status: 404 });
     if (campaign.ownerId !== session.user.id && session.user.role !== 'admin') {
       return new Response('Forbidden', { status: 403 }); // ownership check, not just "logged in"
     }
     // ... proceed
   }
   ```
   The two failure patterns to grep for: (a) a route that checks `session` exists but never checks the session user actually owns/can-access the specific resource by ID, and (b) a route that relies on the UI simply not rendering a delete button for non-owners — server-side checks are the only ones that count. Server actions need the same `auth()` plus ownership check inside the action body — they are reachable by a direct POST, so a check on the page that renders the form doesn't protect them ([Next.js: Data Security](https://nextjs.org/docs/app/guides/data-security)).

6. **Password reset / OTP rate limits** — these endpoints are a favorite target for enumeration and brute force. Confirm a limiter is applied (see [[rate-limit-audit]] for defaults) — at minimum: rate-limit by IP *and* by the target email/phone, and return the same response whether or not the account exists (don't leak account existence via response differences or timing).

7. **Secret rotation** — replacing `AUTH_SECRET` (formerly `NEXTAUTH_SECRET`) outright invalidates all existing JWT sessions immediately (users get logged out) — that's the right move after a suspected leak. For a *planned* rotation, keep the old secret alongside the new one: Auth.js accepts `secret` as an array, uses the first secret that decrypts a token, and its docs say the newer secret goes at the start of the array, where it's used for all new sessions ([Auth.js reference: `secret`](https://authjs.dev/reference/core#secret)). From env, Auth.js builds that array from `AUTH_SECRET` plus `AUTH_SECRET_1` to `AUTH_SECRET_3`, placing the numbered ones first with the highest number at the front (`setEnvDefaults` in the Auth.js source). Drop the old secret once existing sessions have expired. Rotate provider client secrets (GitHub/Google OAuth app secrets) independently on their own suspected-compromise timeline.

8. **Session invalidation on privilege change** — when a user's role changes (promoted to admin, downgraded, banned), a JWT-strategy session keeps its old role claim until the token naturally expires or refreshes. Mitigate by either: keeping JWT `maxAge` short (e.g., 1 hour) with refresh, or checking current role from the database on sensitive actions rather than trusting the JWT claim verbatim, or switching that specific check to a DB lookup:
   ```ts
   const freshUser = await prisma.user.findUnique({ where: { id: session.user.id }, select: { role: true } });
   if (freshUser?.role !== 'admin') return new Response('Forbidden', { status: 403 });
   ```

## Audit workflow over an existing app

1. Grep every `app/api/**/route.ts` and every server action (files or functions marked `'use server'`) for a call to `auth()` — flag any that mutate/read protected data without one.
2. For each route that has `auth()`, confirm it checks *ownership/role*, not just *presence* of a session.
3. Grep for `NEXTAUTH_SECRET`/`AUTH_SECRET` usage — confirm it's read from env, never hardcoded or committed.
4. Check `.env`/`.env.local` are gitignored; check no OAuth client secret appears in any client component or bundled JS (`grep -r "client_secret\|CLIENT_SECRET" app/`, scoped to files that ship to the browser).
5. Test session invalidation manually: change a user's role in the DB, confirm behavior on their next request to a sensitive route (should re-check, per step 8 above).
6. Confirm rate limits on `/api/auth/*` reset/verify flows — reference [[rate-limit-audit]].

## Output / Evidence

Report to the user as a table: route, session check present (Y/N), ownership/role check present (Y/N), rate limit present (Y/N for auth-adjacent routes). Flag any route missing an ownership check as high-priority regardless of how the rest of the audit goes.

## Stop Conditions

- Found a route with no auth check at all handling user data mutation — flag as a security bug immediately, don't bundle it in with routine findings; confirm with the user before any public disclosure or fix timeline commitment.
- OAuth client secret found in client-shipped code — stop and treat as a credential leak: rotate the secret at the provider immediately, then fix the code.
- Any place storing plaintext passwords or unhashed reset tokens — stop, this is a fundamental fix, not a hardening tweak.
