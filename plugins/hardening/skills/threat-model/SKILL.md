---
name: threat-model
description: "Use when a new feature, route, integration, or data flow is about to be designed or built and nobody has written down who could abuse it and how. Triggers: a spec or plan with no security section, a PR that adds a trust boundary (new input, new external service, new privileged action), a launch review that asks 'what could go wrong', or a request to 'threat model' something."
---

# Threat Model

## Overview

A threat model is a one-page table written **before** code: what we are protecting, where untrusted input crosses into trusted code, who would attack it, and which control answers each threat. Thirty minutes here decides which of the other `hardening` gates a feature needs. Skipping it means every other audit runs blind, checking controls nobody chose on purpose.

Check for a repo-local threat model template or process first (`docs/threat-model.md`, `SECURITY.md`, `AGENTS.md`, a `threat-model` skill in the repository). It is authoritative when present; this skill is the fallback.

If a sibling skill named below is not installed, perform its check from the description given here or record it as an open item. Never skip the control because the skill is missing.

## When to use

- A spec, plan, or issue describes a feature and has no security section.
- A change adds a **trust boundary**: a new user input, file upload, webhook, third-party API, LLM call, background job, or admin action.
- Pre-launch review on a product that has never had one.
- Someone asks "is this safe?" and the honest answer is "nobody has looked."

Not for: reviewing an existing implementation line by line (that is `review-slop` or a security review), or auditing a single control in depth (the sibling skills below).

**Scope when a new feature sits on existing code:** model the feature, plus every existing route, tool, or config the feature reuses or touches. Flaws elsewhere in the repo go in a short "Noticed" list with the sibling skill that owns them; they are not rows.

## Workflow

1. **Scope in one paragraph.** Name the feature, the assets it touches (user data, credentials, money, model access, reputation), and the actors: anonymous visitor, authenticated user, another tenant, an insider, a compromised dependency, an automated agent. Keep the asset list honest: "the Anthropic API bill" is an asset.

2. **Draw the boundaries.** List every point where data moves between trust levels, and give each an ID (B1, B2, ...). With a spec and no code, read the spec's stories and implementation notes and extract the crossings from the prose: who uploads, who receives, which external services are called, which actions a non-owner can trigger. With code, list the source directories first (`git ls-files | cut -d/ -f1 | sort -u`) and search them for the usual crossings:
   ```bash
   # inputs: request handlers, uploads, webhooks, outbound calls, LLM and tool output
   grep -rnE "req\.(body|query|params|json|formData)|request\.(json|formData)|searchParams|multipart|params\.|await .*\.json\(\)" --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --include='*.py' --include='*.rb' --include='*.go' --exclude-dir=node_modules --exclude-dir=.git .
   grep -rnE "webhook|fetch\(|axios|generateText|streamText|tool\(|sendEmail|s3|putObject" --include='*.js' --include='*.mjs' --include='*.ts' --include='*.tsx' --include='*.py' --include='*.rb' --include='*.go' --exclude-dir=node_modules --exclude-dir=.git .
   ```
   Each crossing becomes a boundary. Common ones: browser to API, API to database, API to third-party service, third-party to webhook endpoint, retrieved content to LLM prompt, LLM output to tool call or rendered HTML.

3. **Enumerate threats per boundary with STRIDE.** For each row ask six questions: can someone **S**poof an identity, **T**amper with data in flight or at rest, **R**epudiate an action (no audit trail), cause **I**nformation disclosure, **D**eny service (or run up a bill), or **E**levate privilege. Write only the threats that are plausible for that boundary; a row with "none" is a legitimate answer when stated.

4. **Rate each threat.** Likelihood (low / medium / high) and impact (low / medium / high). Impact is **high** when the harm is irreversible, crosses tenants, loses a credential, or costs real money without a cap; **low** when it is recoverable and contained to one user. A threat **blocks** the feature if it is high/high, or if it reaches an irreversible action or another tenant's data regardless of its other rating.

5. **Assign a control and an owner skill.** Every threat gets a concrete control, or an explicit accepted risk with a reason and an approver. A blocking threat cannot be accepted by the modeler; if no control is known, or the spec leaves the control undecided (for example whether links need login), its status is OPEN-BLOCKS with the decision that is needed. Map controls to the sibling gate that verifies them:

   | Threat class | Control | Verified by |
   |---|---|---|
   | Abuse of a paid or auth endpoint | Rate limit keyed on the right dimension | `rate-limit-audit` |
   | Spoofed or over-scoped identity | Per-route authorization, session config | `auth-hardening` |
   | Forged or replayed external event | Signature check, idempotency key | `webhook-reliability` |
   | Data collected or stored it should not be | Minimization, retention, export/delete | `privacy-audit` |
   | Credential or PII leaks through bundle, logs, responses, git | Scrubbing, server-only secrets | `secrets-leak-audit` |
   | Clickjacking, XSS reach, mixed content | CSP, HSTS, frame and MIME headers | `security-headers` |
   | Untrusted content steering an LLM or its tools | Output gating, tool allowlists, approval | `llm-app-security` |
   | Compromised dependency or agent connection | Supply-chain scan, least-privilege tooling | `exposure-scan`, `agent-tooling-review` |

6. **Write it where the spec lives.** The table goes into the feature's spec, issue, or `docs/threat-model.md`, not a chat message. End with the gate list and a record line: `YYYY-MM-DD, author (person, or agent name and model), boundaries covered, accepted risks with approver`. Future PRs that touch a boundary update the row. If asked not to modify the repo, return the text and the intended file path instead.

   **Gate list:** the distinct sibling skills named in the table's "Verified by" column, each with the boundary IDs it must verify, in the order they should run (blocking items first). This is the answer to "which other gates does this feature need".

## Output

A table with these columns:

```
| # | Boundary | Actor | Threat (STRIDE letter) | Likelihood | Impact | Control | Verified by | Status |
```

Status is one of OPEN-BLOCKS, OPEN, MITIGATED, ACCEPTED. Under the table, one line per boundary listing all six STRIDE letters with the threat row number or "none", so "none" is recorded where true. Then the one-paragraph scope, the accepted risks with reasons and approvers, the "Noticed" list, and the gate list. If the table has zero rows, the scope paragraph was wrong; every feature that takes input has at least one boundary.

## Checklist

- [ ] Assets named, including cost and reputation where relevant
- [ ] Every input and every external call appears as a boundary row
- [ ] Each boundary has STRIDE applied, with "none" written out where true
- [ ] Every blocking threat has a control or is marked OPEN-BLOCKS with the decision needed; none is accepted by the modeler
- [ ] Each control names the sibling skill that will verify it
- [ ] Table, STRIDE line per boundary, and gate list committed next to the spec, with the record line (or, when the repo is read-only, returned with the intended path)

## Common mistakes

- **Modeling the happy path.** The table lists features, not attacks. Each row must name an actor doing something unwanted.
- **Treating the client as trusted.** "The UI only shows the button to admins" is not a control. The server check is.
- **Forgetting the model is an input.** LLM output that reaches a tool, a database, or rendered HTML is untrusted input and gets its own boundary row.
- **Forgetting the bill.** Denial of wallet on an LLM or email endpoint is a denial-of-service threat with a dollar sign.
- **Accepting risk silently.** An accepted risk without a written reason is an unmitigated threat someone will rediscover.

## Stop conditions

- Untrusted content can reach an LLM that has tools with side effects and no row covers it: stop, open `llm-app-security` before design continues.
- A boundary's only control is "we trust the client" or "nobody would try that": stop, it needs a real control or a written accepted risk.
- The feature stores a new category of personal data and no row sends it to `privacy-audit`: stop, that audit decides whether to collect it at all.
