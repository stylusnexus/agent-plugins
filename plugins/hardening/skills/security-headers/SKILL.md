---
name: security-headers
description: "Use when checking or setting HTTP security headers on a deployed site or API: Content-Security-Policy, Strict-Transport-Security, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy. Triggers: pre-launch review, a new domain or reverse proxy, a scanner report (Mozilla Observatory, securityheaders.com) with a bad grade, an XSS or clickjacking finding, or an auth response that browsers are caching."
---

# Security Headers

## Overview

Headers are the cheapest control in the stack and the one most often set on localhost and lost in production: a reverse proxy strips them, a CDN overrides them, a second framework serves the API without them. This skill checks the **deployed** response, finds the layer that owns each header, and rolls out Content-Security-Policy without breaking the app.

Check for a repo-local header policy first (`docs/security-headers.md`, `AGENTS.md`, `SECURITY.md`, a checked-in CSP, or a repo-local `security-headers` skill). It is authoritative when present; this skill is the fallback.

Status words used throughout: **PASS** (seen in a live response), **FAIL** (seen wrong, live or in config), **UNVERIFIED** (not seen in a live response). A config read alone can prove a FAIL but never a PASS.

## Workflow

1. **Capture the deployed response.** Find the real origin (deploy config, README, environment settings), one real page, one real API route, and one real static asset (read its name from the page source). Set `ORIGIN`, `PAGE`, `API`, and `ASSET` to those, then:
   ```bash
   for url in "$ORIGIN$PAGE" "$ORIGIN$API" "$ORIGIN$ASSET"; do
     echo "== $url"; curl -sSI "$url" | tr -d '\r' | grep -iE '^(content-security-policy|strict-transport|x-frame|x-content-type|referrer-policy|permissions-policy|cache-control|access-control-|set-cookie|server|x-powered-by)'
   done
   ```
   For authenticated API responses, repeat the API request with a session cookie from a test account (`curl -sSI -H "Cookie: $TEST_COOKIE"`); never a real user's cookie. Save the raw output; it is the before-evidence.

   **No deployed origin yet?** Run in static mode: read the config (step 3), report every header as FAIL or UNVERIFIED, and state that launch readiness cannot be PASS until a staging capture exists. A locally started production build (`next start`, `npm run preview`) is supplemental evidence only: label it "local, not deployed", because the host or CDN will add, remove, or override headers.

2. **Score each header against the baseline.**

   | Header | Baseline | Fail if |
   |---|---|---|
   | `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` (add `preload` only once every subdomain is HTTPS) | missing, or `max-age` under 6 months |
   | `Content-Security-Policy` | `default-src 'self'`; explicit `script-src`, `connect-src`, `img-src`, `frame-ancestors 'none'`, `base-uri 'self'`, `form-action 'self'`; nonces or hashes for inline scripts | missing, `script-src` contains `'unsafe-inline'` or a bare scheme or `*`, `img-src *`, or enforcing CSP never reached (see step 4) |
   | `X-Frame-Options` | `DENY` (or `SAMEORIGIN` if the app embeds itself) | missing and CSP has no `frame-ancestors` |
   | `X-Content-Type-Options` | `nosniff` | missing on any response |
   | `Referrer-Policy` | `strict-origin-when-cross-origin` | missing, or `unsafe-url` |
   | `Permissions-Policy` | deny what the app does not use: `camera=(), microphone=(), geolocation=()` | missing on pages |
   | `Cache-Control` on auth and user-specific API responses | `no-store` | cacheable responses carrying session data |
   | `Server`, `X-Powered-By` | absent (for example `poweredByHeader: false`) | present with a version string; a bare framework name is a low-severity finding |

3. **Find the owning layer for each header.** Headers can be set in the framework, middleware, route handlers, the platform, a CDN, or a proxy; two layers setting the same header produce duplicates or a silent override. Search the whole repo for every header name in the table, not a fixed file list:
   ```bash
   grep -rniE "content-security-policy|frame-ancestors|x-frame-options|strict-transport|x-content-type|referrer-policy|permissions-policy|access-control-|poweredByHeader|headers\.set|setHeader|headers\(\)" \
     --include='*.js' --include='*.mjs' --include='*.cjs' --include='*.ts' --include='*.tsx' --include='*.json' --include='*.toml' --include='*.yaml' --include='*.yml' --include='*.conf' --include=Caddyfile --include=_headers \
     --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=.git .
   ```
   Every file in the output is a candidate owner. If the same header appears in two files with different values, that is a conflict to resolve before anything else.
   Pick **one** owner per header and record it. Prefer the layer closest to the app (framework config or middleware) so headers travel with the code and survive a hosting change.

4. **Roll out CSP in two steps.** Never ship a strict CSP straight to enforcing mode on a live app.
   - Step one: `Content-Security-Policy-Report-Only` with the intended policy and a `report-to` or `report-uri` endpoint. Run it for a release cycle. Read the reports; every violation is either a real inline script to nonce or an origin to allowlist.
   - Step two: promote to `Content-Security-Policy` once the report stream is quiet. Keep `Report-Only` alongside for the next tightening.
   For frameworks that inject inline scripts, use a per-request nonce (`'nonce-<base64>'`) or `'strict-dynamic'`; `'unsafe-inline'` on `script-src` cancels the point of the header.
   **Launch rule:** a Report-Only CSP that has not yet been promoted counts as CONDITIONAL, not PASS. Launching on it requires every other header to PASS, a staging Report-Only run with its reports read, and a written, dated acceptance of the gap naming who accepted it.

5. **Check the API surface separately.** API routes often bypass page middleware. Verify `X-Content-Type-Options: nosniff` and `Cache-Control: no-store` on authenticated JSON responses, and that CORS (`Access-Control-Allow-Origin`) is a named origin, not `*`, wherever credentials are accepted.

6. **Re-capture and diff.** Rerun step 1 after the change on the same three URLs. The after-evidence is the diff of the two captures plus a third-party scan link (Mozilla Observatory or securityheaders.com) if the site is public.

## Checklist

- [ ] Live production (or staging) headers captured for a page, an API route, and a static asset
- [ ] HSTS present with a one-year `max-age`
- [ ] CSP present; `script-src` has no `'unsafe-inline'` and no wildcard; `frame-ancestors` set
- [ ] `nosniff` on every response class, including API and assets
- [ ] `Referrer-Policy` and `Permissions-Policy` set on pages
- [ ] Authenticated API responses are `no-store`
- [ ] Each header has exactly one owning layer, recorded
- [ ] Before and after captures saved as evidence

## Output

A table: header, current value, owning layer, status (PASS / FAIL / UNVERIFIED). When changes were made, add before and after columns. Attach the raw `curl -sSI` captures. A header claimed without a live capture is UNVERIFIED, and a review with no live capture ends with the verdict "not verified for launch", never "ready".

## Common mistakes

- **Testing localhost.** Dev servers add and strip headers differently from production. A local production build is supplemental evidence; only the deployed response earns a PASS.
- **Shipping an allowlist CSP that is really a wildcard.** `script-src 'self' 'unsafe-inline' https:` blocks nothing an attacker needs.
- **Setting `X-Frame-Options` and forgetting `frame-ancestors`.** Modern browsers honor CSP first; set both and make them agree.
- **HSTS `preload` on day one.** Preload is near-irreversible; a single HTTP-only subdomain becomes unreachable. Earn it after `includeSubDomains` has run clean.
- **Caching the login response.** A `Set-Cookie` response without `Cache-Control: no-store` can be served from a shared cache to the next user.

## Stop conditions

- Enforcing CSP would break the app and the proposed fix is `'unsafe-inline'`: stop, ship `Report-Only` and nonces instead; do not mark the header done.
- Headers are set in two layers with different values: stop, pick the owner and remove the other before adding more.
- Any authenticated response is cacheable by a shared cache: stop, this is a session-leak path and blocks launch.
