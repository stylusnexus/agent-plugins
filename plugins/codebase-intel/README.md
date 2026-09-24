# Codebase Intelligence

Four skills for building an accurate picture of a codebase — and of the libraries it leans on — *before* committing to a change.

The failure these guard against is the same in both directions: acting on a mental model that was never checked. Inside the repo, that's refactoring around structure you assumed; outside it, that's calling an API the way you remember it working.

---

## The skills

| Skill | Use it when |
|---|---|
| `codebase-health` | Onboarding somewhere unfamiliar, planning a refactor, or diagnosing why one area keeps breaking. Reports complexity hotspots, churn, bus factor, and velocity from git history. |
| `codebase-architecture-scanner` | You need architecture documentation that doesn't exist yet — layered high-level and detailed docs, with C4 context and sequence diagrams. |
| `grill-with-docs` | A plan is drafted and needs challenging against the domain model that's already there, sharpening terminology and updating docs rather than inventing parallel vocabulary. |
| `read-the-damn-docs` | Anything touching a third-party API, library, framework, CLI, cloud service, or provider SDK. Goes to current documentation instead of trusting recall. |

---

## Rule ownership

| Skill | Owns |
|---|---|
| `codebase-health` | Quantitative repository signals — complexity, churn, hotspots, bus factor |
| `codebase-architecture-scanner` | Structural description — components, layers, boundaries, diagrams |
| `grill-with-docs` | Adversarial review of a plan against the existing domain model and terminology |
| `read-the-damn-docs` | Everything *outside* the repository — third-party behavior, versions, current APIs |

The split that matters most: **`codebase-health` measures, `codebase-architecture-scanner` describes.** Health tells you where the pain is concentrated; the scanner tells you how the thing is put together. Reach for health when deciding *whether* and *where* to change something, and the scanner when you need to explain the system to someone — including your future self.

`read-the-damn-docs` is the only one that looks outward, and it's the cheapest habit in the pack: a wrong assumption about a library's behavior survives code review, because reviewers assume it too.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install codebase-intel@stylus-nexus
```

Skills are namespaced: `/codebase-intel:codebase-health`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add codebase-intel@stylus-nexus
```

In Codex, type `$codebase-health` (or any skill name after `$`) to use a skill, or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill codebase-architecture-scanner codebase-health grill-with-docs read-the-damn-docs
```

Skills arrive un-namespaced on this path, so they invoke as `/codebase-health`.

## Prerequisites

- **`git`** — `codebase-health` reads history for churn and bus-factor signals
- **Network access** — `read-the-damn-docs` fetches current documentation
- Diagram output is Mermaid, which renders natively in GitHub, and in the artifacts produced by the `reporting-comms` pack

## License

MIT © Stylus Nexus Holdings LLC — see the [repository LICENSE](../../LICENSE).
