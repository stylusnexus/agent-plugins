# Hardening

Six pre-launch gates for the unglamorous security work — the failures that aren't clever, don't make headlines, and ship to production constantly.

None of this is exotic. A missing rate limit on an endpoint that calls a paid API, a webhook with no signature check, a compromised transitive dependency, an API key that turns up in a log line. These are cheap to check and expensive to discover in the wild.

---

## The skills

| Skill | Use it when |
|---|---|
| `rate-limit-audit` | Before launch, or after adding an endpoint that calls a paid API (LLM, email, SMS) or handles auth. Inventories every such endpoint and checks each actually has a limit. |
| `exposure-scan` | Periodically, and after any dependency change. Checks installed packages across npm, Go, PyPI, RubyGems, and MCP servers against threat-intelligence catalogs for known-compromised releases. |
| `auth-hardening` | Auth is in place and needs auditing — session and cookie configuration, CSRF, OAuth scopes, per-route protection. |
| `webhook-reliability` | Designing or reviewing webhooks in either direction: signature verification, idempotency, retry and backoff, dead letters, monitoring. |
| `privacy-audit` | User data is collected and someone needs to say exactly what and where. Produces the inventory and checks it against the code and infra — not against what the privacy policy claims. |
| `readiness-review` | Before launch, or on a recurring schedule, to answer "is the code healthy and can a user actually do the core jobs?" in one report. Read-only: scans, a reviewer pass over a secret-free copy, a look-only walk of the live product, and a findings list you file yourself. |

---

## Rule ownership

| Skill | Owns |
|---|---|
| `rate-limit-audit` | Abuse and cost ceilings on endpoints |
| `exposure-scan` | Supply chain — what you installed and whether it's known-compromised |
| `auth-hardening` | Identity, sessions, and per-route access control |
| `webhook-reliability` | Trust and delivery guarantees at system boundaries |
| `privacy-audit` | What data exists, where it lands, and who can reach it |
| `readiness-review` | The overall launch verdict: code health, live database structure, and whether a user can do the core jobs |

Two of these are about **cost and abuse** (`rate-limit-audit`, `exposure-scan`), two about **trust boundaries** (`auth-hardening`, `webhook-reliability`), one about **data itself** (`privacy-audit`), and one steps back to ask whether the whole thing is ready (`readiness-review`). They compose but don't overlap: a rate-limited endpoint can still leak PII, and a correctly-scoped OAuth flow says nothing about whether your dependencies are clean.

The one worth running first is `privacy-audit`, because it's the only one whose finding might be *"we shouldn't be collecting this at all"* — and that answer changes what the other five need to protect. `readiness-review` is the one to run last and then on a schedule: its report points at which of the others a finding belongs to.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install hardening@stylus-nexus
```

Skills are namespaced: `/hardening:rate-limit-audit`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add hardening@stylus-nexus
```

In Codex, type `$` and a skill name to use it (`$hardening:rate-limit-audit`; Codex prefixes plugin skills with the pack name), or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill auth-hardening exposure-scan privacy-audit rate-limit-audit readiness-review webhook-reliability
```

Skills arrive un-namespaced on this path, so they invoke as `/rate-limit-audit`.

## Prerequisites

`exposure-scan` shells out to [`bumblebee`](https://github.com/perplexityai/bumblebee), which must be installed and on `PATH`:

```bash
go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest
```

Its bundled threat-intelligence catalogs are pinned to the installed version while upstream publishes updates far more often, so the skill refreshes them before scanning.

`readiness-review` needs `python3` (with [`uv`](https://docs.astral.sh/uv/) recommended, so its scripts fetch their own two dependencies), the `gh` CLI signed in for the GitHub facts, and optionally a browser tool (Claude in Chrome, Chrome DevTools MCP, or Playwright MCP) for the product walk and a read-only Postgres role for the live-database check. Each missing piece is reported as not checked; the run continues. Product specifics go in a `.readiness-review.yaml` in the reviewed repo — start from its [config template](skills/readiness-review/references/config-template.yaml).

The other four skills need only repository access and, for `privacy-audit`, visibility into where data actually lands (database, logs, analytics, third-party processors).

## Scope note

These are audits and checklists — they find and report. None of them applies a fix without you deciding to, `readiness-review` never files an issue or writes to a database in any mode, and none should be treated as a substitute for a real security review of anything genuinely sensitive.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
