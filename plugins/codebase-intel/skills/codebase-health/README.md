<!-- skill-readme:begin -->
# codebase-health

Use when onboarding to an unfamiliar codebase, before major refactors, during periodic health checks, or when diagnosing why code keeps breaking. Also use when assessing bus factor, churn hotspots, or development velocity on any git repository.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [codebase-intel](../../README.md) pack.

## When and how to use it

**Use it when:** You join a new repo and want to know where it hurts before you read code.

**Try:** `/codebase-health --since "6 months ago" --top 10`

**Skip it when:** The folder has no git history, or you need a code-level bug search.

## What it looks like

*Example output, invented data.*

```text
## Codebase Health Report — example-shop
Period: 1 year ago to now | Top: 5 per category

### Priority Targets (churn + bugs)
  src/checkout/totals.ts        churn 64   bug fixes 19
  src/api/orders/route.ts       churn 41   bug fixes 11

### Bus Factor
  dev-a 58%   dev-b 21%   dev-c 9%   others 12%
  Risk: HIGH (top 2 own 79%)

### Velocity Trend
  2025-02 88 ... 2025-11 61   2025-12 47   2026-01 39   <- down 3+ months

### Firefighting Index
  31 of 702 commits (4.4%) — MODERATE
```

How the report grades each signal:

| Signal | Threshold | Read it as |
|---|---|---|
| File in churn and bug lists | appears in both | Highest-risk code: refactor or add tests first |
| Bus factor | top 2 contributors own over 60% | Knowledge silo |
| Firefighting index | LOW under 2% · MODERATE 2–5% · HIGH over 5% | Deploy confidence |
| Velocity | dropping for 3+ months | A team question, not a code one |

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install codebase-intel@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install codebase-intel@stylus-nexus` do the same. This installs the whole codebase-intel pack, so codebase-architecture-scanner, grill-with-docs and read-the-damn-docs come with it.

Call it as `/codebase-intel:codebase-health`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **codebase-intel**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add codebase-intel@stylus-nexus
```

This installs the whole codebase-intel pack, so codebase-architecture-scanner, grill-with-docs and read-the-damn-docs come with it. In Codex, type `$` and the skill name (`$codebase-intel:codebase-health`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill codebase-health
```

Skills arrive without a pack prefix: `/codebase-health` in most agents and `@codebase-health` in Windsurf. opencode shows `/codebase-health` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/codebase-intel/skills/codebase-health .agents/skills/
```

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Runs in a remote sandbox without your local repo, git remotes or credentials.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No access to your local repo or git and gh credentials by default.

</details>
<!-- skill-readme:end -->
