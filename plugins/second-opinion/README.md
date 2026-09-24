# Second Opinion

Five skills built on one premise: **a single model's confident answer is not evidence.**

Confidence and correctness are only loosely related, and an agent that is wrong is usually wrong fluently. These skills exist to introduce a second perspective before a decision hardens — whether that's a competing plan, an independent panel, a spec checked against reality, or a bug reproduced before anyone theorises about it.

---

## The skills

| Skill | Use it when |
|---|---|
| `llm-council` | A question, idea, or decision is consequential enough to want five advisors analysing it independently before synthesis — rather than one answer delivered confidently. |
| `plan-arbiter` | Two or more plans are on the table and someone has to compare, cross-review, merge, judge, or arbitrate between them. Picks on reasoning, not on whichever was written last. |
| `spec-review` | A spec or requirements doc is drafted or about to be implemented. Verifies its claims against the real codebase — catching wrong data-model assumptions before code embeds them. |
| `agent-watchdog` | Another agent's work needs watching, auditing, comparing, or fixing, from a session ID or transcript. |
| `debug-feedback-loop` | A bug needs a fast, deterministic pass/fail signal **before** hypothesising about causes — the step most debugging skips. |

---

## Rule ownership

| Skill | Owns |
|---|---|
| `llm-council` | Multi-advisor deliberation on an open question, and synthesis of their disagreement |
| `plan-arbiter` | Adjudication between competing *plans* that already exist |
| `spec-review` | Checking a written spec's factual claims against the codebase |
| `agent-watchdog` | Oversight of *another agent's* execution and output |
| `debug-feedback-loop` | Establishing reproduction before diagnosis |

The distinction that matters: **`llm-council` opens a question, `plan-arbiter` closes one.** Reach for the council when you don't yet know the right shape of the answer and want genuinely independent takes; reach for the arbiter when candidate plans already exist and one has to win.

`spec-review` is the cheapest of the five and catches the most expensive class of error — a spec that assumes a table, column, or relationship that isn't there. That assumption survives review because reviewers read the spec, not the schema.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install second-opinion@stylus-nexus
```

Skills are namespaced: `/second-opinion:plan-arbiter`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

In Codex, type `$` and a skill name to use it (`$second-opinion:plan-arbiter`; Codex prefixes plugin skills with the pack name), or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill agent-watchdog debug-feedback-loop llm-council plan-arbiter spec-review
```

Skills arrive un-namespaced on this path, so they invoke as `/plan-arbiter`.

## Prerequisites

- **Multiple model access** for `llm-council` — the value comes from advisors that genuinely differ, so pointing all five at one model defeats the purpose.
- **`git`** and repository access for `spec-review`, which reads the codebase rather than trusting the spec's description of it.

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
