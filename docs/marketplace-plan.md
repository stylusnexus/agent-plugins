# Marketplace plan

How skills get curated, packaged, and published through this repository. Supersedes the working notes in `Project Notes/marketplace/`, several of whose premises did not survive contact with the repos — see [Corrections](#corrections).

---

## Plain-English summary

We have a large pile of accumulated agent skills. Most are noise; a minority are genuinely good. The job is to take the ones actually used across the development lifecycle, strip anything specific to our own projects, group them into small coherent packs, and publish them so any coding agent can install them.

This repository is the distribution layer. A pack is a directory under `plugins/`, containing plain markdown skills plus two small manifest files. Those two manifests are what let a single copy of a skill install into Claude Code, into Codex, and — because the Skills CLI reads one of the same manifests — into roughly seventy other agents including Cursor, Copilot, and Gemini CLI. Nothing is duplicated per host.

The rule that governs everything: **a published skill must not assume our conventions.** Not our branch names, not our stack, not our repo layout. Where a project genuinely needs different behavior, the skill defers to a repo-local version of itself.

---

## Layout

```
agent-plugins/
├── .claude-plugin/marketplace.json    # Claude index
├── .agents/plugins/marketplace.json   # Codex index
└── plugins/<pack>/
    ├── .claude-plugin/plugin.json     # Claude manifest
    ├── .codex-plugin/plugin.json      # Codex manifest — separate dir, required
    ├── skills/<name>/SKILL.md
    └── README.md
```

Packs may either live in-repo under `plugins/` or in their own repository pinned to a release tag. Both forms coexist in the indexes; in-repo is the default for skill-only packs, and a separate repo is warranted when a pack ships executable code (as `work-plan` does with its Python CLI and VS Code viewer).

### Verified manifest contracts

| Host | Index | Source form |
|---|---|---|
| Claude Code | `.claude-plugin/marketplace.json` | `"source": "./plugins/<pack>"` |
| Codex | `.agents/plugins/marketplace.json` | `{"source": "local", "path": "./plugins/<pack>"}` — must start `./` and stay inside the marketplace root |
| Skills CLI | reads `.claude-plugin/marketplace.json` | discovers `plugins/<pack>/skills/<name>/SKILL.md` |

Claude and Codex read **different manifest directories** (`.claude-plugin/` vs `.codex-plugin/`), so a dual-host pack carries both. Claude namespaces plugin skills as `/<pack>:<skill>`; the Skills CLI installs un-namespaced, so skills invoke as `/<skill>` on that path.

Validate before publishing:

```bash
claude plugin validate ./plugins/<pack>    # plugin manifest + every SKILL.md
claude plugin validate .                   # marketplace manifest
npx skills add . --list                    # confirm discovery + descriptions
```

---

## Authoring rules

**Global means global.** No project names, and — the harder test — no project *assumptions*. A brand grep is not sufficient; `review-merge-pipeline` shipped "all PRs target `dev` (not `main`)" with no brand name anywhere in it. Detect the repository's conventions, state the fallback, and accept an override flag.

**Defer to repo-local.** Each skill states that a repo-local version of itself is authoritative when present. Global skills are the fallback, not the law.

**One rule, one owner.** Skills in a pack must not compete for the same trigger. Record ownership in the pack README and let the others name only the handoff. This is why a skill needed by two packs argues for merging the packs rather than duplicating the skill — duplication leaves two identical descriptions fighting over one intent.

**Reference siblings by backticked name**, never as `/skill-name`. Bare slash references break under plugin namespacing.

**Frontmatter is load-bearing and fails silently.** An unquoted YAML value containing `": "` drops the *entire* frontmatter block — the skill then loads with no name and no description and can never auto-trigger. `claude plugin validate` catches this; nothing at runtime does.

**`SKILL.md` is case-sensitive** on every filesystem that matters, even where it resolves locally on macOS.

---

## What is never published

**Third-party skills.** The planning and TDD primitives — `brainstorming`, `writing-plans`, `test-driven-development`, `subagent-driven-development`, `systematic-debugging` — belong to the superpowers plugin. Packs that need them declare a dependency in their README; they are never copied. The same holds for Anthropic's `mcp-builder`, Supabase's `supabase-postgres-best-practices`, and the PostHog and Neon vendor skills. `defect-scan` and `work-plan` are already published from their own repositories and are referenced, not re-shipped.

**Persona-pack templates.** Roughly sixteen skills and ten agents sharing a `tools: ["*"]` signature are widely-circulated public packs, not original work.

**Proprietary material.** Anything that would leak internal or security detail.

**Personal conventions.** Workflow glue specific to one person's setup stays in the private `evemcgivern/agent-skills` repository.

---

## Packs

| Pack | Status | Contents |
|---|---|---|
| **ship-pipeline** | shipped | `start-issue`, `db-truth`, `prove-it`, `review-merge-pipeline`, `deploy`, `db-migration-safety`, `backup-verify` |
| Reporting & Comms | candidate | Output-readability skills — visual plans, recaps, writing clarity |
| Codebase Intelligence | candidate | Codebase health, architecture scanning, docs-grounding |
| Second Opinion | candidate | Multi-model review and adjudication |
| Hardening | candidate | Rate limits, exposure scanning, auth review |
| Release Ops | candidate | Versioning, publishing, changelog |

Candidates are ordered by how little rework they need, not by ambition. Each needs an assumption audit before it ships.

---

## Corrections

Recorded so the disproven premises don't get re-adopted from the older notes:

- **This repository was described as index-only.** It now hosts packs directly under `plugins/`. Both the relative-path form (Claude) and the `local` source form (Codex) are officially supported, so in-repo hosting costs no reach.
- **`shipping-with-agents` and `testing-with-agents` were described as bundling homes.** They are static marketing websites — `index.html`, `style.css`, `logo.png`. The "20+ skills" figure is website copy, not directories. `full-starter` is a Next.js and Playwright starter with no `skills/` directory.
- **Reach was assumed to require per-host installers.** The Skills CLI already covers ~70 agents from the Claude manifest, so Gemini CLI, Cursor, and Copilot need no bespoke shims.
