<!-- skill-readme:begin -->
# efficient-frontier-routing

Routes each task to a suitable model tier in Claude Code, Codex, or another agent that can start subagents on a chosen model (for example Gemini CLI or Antigravity CLI), following the user's routing preferences. Keeps small tasks local, delegates discovery, routine coding, and testing to cheaper subagents, and sends difficult decisions and risky reviews to a stronger one. Use when deciding whether to delegate, writing subagent handoffs, or setting routing preferences, or when asked to "save tokens", "use cheaper models", "fan out subagents", "stay inside my quota", or "efficient-frontier-routing help".

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app: No subagents or model choice in the app, so nothing is routed. ChatGPT: No subagents or model choice documented for ChatGPT, so nothing is routed. Other agents: Routing needs per-agent model choice, documented for Cursor, Gemini CLI/Antigravity CLI and opencode but not for Copilot, Windsurf or Cline.

Part of the [second-opinion](../../README.md) pack.

## When and how to use it

**Use it when:** You want cheaper models on routine steps and a stronger model on hard ones.

**Try:** `Use efficient-frontier-routing: scan the repo with a cheap agent, then review the fix with a strong one.`

**Skip it when:** The task is small. Doing it in the current session costs less than a handoff.

## What it looks like

*Example output, invented data.*

```text
Task: fix failing checkout tests, tighten the refund rule
Preferences: discovery Haiku · implementation Sonnet · risky review Opus (high)
             · at most 2 subagents at once

Step                                   Ran on              Why
Run suite, cluster failures            Haiku subagent      discovery
Map where refund logic lives           Haiku subagent      discovery
Fix stale fixture                      main session        too small to hand off
Review refund change before editing    Opus, effort high   billing is high-risk
Apply change, rerun tests, reopen      main session        verify, don't forward
  the two files the reviewer flagged
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install second-opinion@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install second-opinion@stylus-nexus` do the same. This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, llm-council, plan-arbiter and spec-review come with it.

Call it as `/second-opinion:efficient-frontier-routing`, or let it start on its own when your request matches.

**Note:** Picks a model per subagent.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **second-opinion**. Plugins do not load in the app's cloud sessions.

**Note:** Picks a model per subagent.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, llm-council, plan-arbiter and spec-review come with it. In Codex, type `$` and the skill name (`$second-opinion:efficient-frontier-routing`), or run `/skills` to pick it.

**Note:** Picks a model per subagent through Codex agent files.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill efficient-frontier-routing
```

Skills arrive without a pack prefix: `/efficient-frontier-routing` in most agents and `@efficient-frontier-routing` in Windsurf. opencode shows `/efficient-frontier-routing` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Routing needs per-agent model choice, documented for Cursor, Gemini CLI/Antigravity CLI and opencode but not for Copilot, Windsurf or Cline.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/second-opinion/skills/efficient-frontier-routing .agents/skills/
```

**Limit:** Routing needs per-agent model choice, documented for Cursor, Gemini CLI/Antigravity CLI and opencode but not for Copilot, Windsurf or Cline.

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** No subagents or model choice in the app, so nothing is routed.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No subagents or model choice documented for ChatGPT, so nothing is routed.

</details>
<!-- skill-readme:end -->
