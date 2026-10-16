# Hardening

Eleven security skills: six pre-launch gates for the unglamorous failures that ship to production constantly, plus five that cover design time and the agent era.

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
| `threat-model` | A feature is being designed and nobody has written down who could abuse it. Produces the boundary-and-threat table before code, and names which other skill verifies each control. |
| `security-headers` | Before launch, or after a proxy or domain change. Captures the deployed response, assigns one owning layer per header, and rolls out CSP report-only first. |
| `secrets-leak-audit` | Before launch, or after a key shows up somewhere it should not. Checks git history, the production bundle, logs and error reports, and API responses. |
| `agent-tooling-review` | An MCP server, plugin, or token is being connected to an agent, or an agent will run unattended. Applies least privilege and a human gate on irreversible actions. |
| `llm-app-security` | A feature sends untrusted content to a model or lets a model act. Maps input-to-sink paths, requires gates on output and actions, and proves them with a public adversarial corpus. |

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
| `threat-model` | Deciding what to defend and which gate checks it |
| `security-headers` | Browser-enforced controls on the deployed response |
| `secrets-leak-audit` | Credentials and personal data leaving through git, bundles, logs, responses |
| `agent-tooling-review` | What an agent is permitted to connect to and do, attended or not |
| `llm-app-security` | What untrusted content can make a model do |

Two of these are about **cost and abuse** (`rate-limit-audit`, `exposure-scan`), two about **trust boundaries** (`auth-hardening`, `webhook-reliability`), one about **data itself** (`privacy-audit`), and one steps back to ask whether the whole thing is ready (`readiness-review`). `threat-model` runs first and decides which of the others a feature needs; its table names the skill that verifies each control. They compose but don't overlap: a rate-limited endpoint can still leak PII, and a correctly-scoped OAuth flow says nothing about whether your dependencies are clean.

The one worth running first is `privacy-audit`, because it's the only one whose finding might be *"we shouldn't be collecting this at all"* — and that answer changes what the others need to protect. `readiness-review` is the one to run last and then on a schedule: its report points at which of the others a finding belongs to.

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
npx skills add stylusnexus/agent-plugins --skill agent-tooling-review auth-hardening exposure-scan llm-app-security privacy-audit rate-limit-audit readiness-review secrets-leak-audit security-headers threat-model webhook-reliability
```

Skills arrive un-namespaced on this path, so they invoke as `/rate-limit-audit`.

## Prerequisites

`exposure-scan` shells out to [`bumblebee`](https://github.com/perplexityai/bumblebee), which must be installed and on `PATH`:

```bash
go install github.com/perplexityai/bumblebee/cmd/bumblebee@latest
```

Its bundled threat-intelligence catalogs are pinned to the installed version while upstream publishes updates far more often, so the skill refreshes them before scanning.

`readiness-review` needs `python3` (with [`uv`](https://docs.astral.sh/uv/) recommended, so its scripts fetch their own two dependencies), the `gh` CLI signed in for the GitHub facts, and optionally a browser tool (Claude in Chrome, Chrome DevTools MCP, or Playwright MCP) for the product walk and a read-only Postgres role for the live-database check. Each missing piece is reported as not checked; the run continues. Product specifics go in a `.readiness-review.yaml` in the reviewed repo — start from its [config template](skills/readiness-review/references/config-template.yaml).

`llm-app-security` and `agent-tooling-review` can use the open-source `@stylusnexus/agentarmor` package as a deterministic scanner, and `llm-app-security` points at the public SecLists `Ai/LLM_Testing` corpora; both are optional. The other skills need only repository access and, for `privacy-audit`, visibility into where data actually lands (database, logs, analytics, third-party processors).

## Scope note

These are audits and checklists — they find and report. None of them applies a fix without you deciding to, `readiness-review` never files an issue or writes to a database in any mode, and none should be treated as a substitute for a real security review of anything genuinely sensitive.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
