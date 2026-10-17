<!-- skill-readme:begin -->
# spec-review

Use when a design spec, plan, or requirements doc is drafted/ratified/about-to-be-implemented and you want a rigorous second-model review that verifies the spec's claims against the real codebase — catching wrong data-model assumptions (scalar-vs-M2M), unverified schema/API claims, missing acceptance criteria, ambiguity, and internal contradictions before code is written. The spec-world analog of /codex:review for PRs.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex partial, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%97%90%20%C2%B7%20ChatGPT%20%E2%9C%96-yellow)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Needs bash, git and the codex CLI on a local repo. Codex: Runs, but the reviewer is Codex reviewing Codex, so the different-model premise is lost, and the default sandbox blocks the network the nested codex call needs. ChatGPT: Needs bash and the codex CLI on a local repo.

Part of the [second-opinion](../../README.md) pack.

## When and how to use it

**Use it when:** A spec is drafted and you want a second model to check its claims against the code.

**Try:** `spec-review .spec-workflow/specs/checkout-redesign -- scrutinize the refund math`

**Skip it when:** You want a review of code changes. Use `/codex:review`.

## What it looks like

*Example output, invented data.*

```text
CODEX SPEC REVIEW: docs/specs/2026-01-10-team-billing-design.md
Verdict: DO NOT SHIP

[CRITICAL] §3 Data model: treats invoice.team_id as one team. The schema has an
           invoice_teams join table (many-to-many). Evidence: prisma/schema.prisma:212
[HIGH]     §5 Acceptance: "refunds work" has no measurable criterion.
[MEDIUM]   §4 says proration is on; §6 says it is off.
[LOW]      §7 migration is not idempotent (no IF NOT EXISTS).

Verified OK
- users.role exists (prisma/schema.prisma:40)
- POST /api/invoices exists (app/api/invoices/route.ts:9)
```

DO NOT SHIP still exits `0`: the exit code says whether the review ran, not what it concluded.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install second-opinion@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install second-opinion@stylus-nexus` do the same. This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, efficient-frontier-routing, llm-council and plan-arbiter come with it.

Call it as `/second-opinion:spec-review`, or let it start on its own when your request matches.

**Note:** Needs an authenticated codex CLI, which supplies the second model.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **second-opinion**. Plugins do not load in the app's cloud sessions.

**Note:** Needs an authenticated codex CLI, which supplies the second model.

</details>

<details>
<summary>Codex (partial)</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, efficient-frontier-routing, llm-council and plan-arbiter come with it. In Codex, type `$` and the skill name (`$second-opinion:spec-review`), or run `/skills` to pick it.

**Limit:** Runs, but the reviewer is Codex reviewing Codex, so the different-model premise is lost, and the default sandbox blocks the network the nested codex call needs.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill spec-review
```

Skills arrive without a pack prefix: `/spec-review` in most agents and `@spec-review` in Windsurf. opencode shows `/spec-review` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Needs bash, git and an authenticated codex CLI.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/second-opinion/skills/spec-review .agents/skills/
```

**Note:** Needs bash, git and an authenticated codex CLI.

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Needs bash, git and the codex CLI on a local repo.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** Needs bash and the codex CLI on a local repo.

</details>
<!-- skill-readme:end -->
