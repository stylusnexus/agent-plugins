<!-- skill-readme:begin -->
# pr-wait

Wait for GitHub PR CI checks to complete, then optionally merge

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Needs gh and your local repo. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** A pull request is open and you want to wait for its CI checks, and maybe merge on green.

**Try:** `/pr-wait 318 true 30`

**Skip it when:** No pull request exists yet, or you want help with the review itself.

## What it looks like

Example output, invented data.

```text
Monitoring PR #318 CI checks...
Check interval: 60s | Max wait: 20 minutes | Auto-merge: enabled

=== Initial Status ===
✅ Build and Test: pass
⏳ E2E Tests: pending

[1] 10:14:00 - 1 check still running:
  ⏳ E2E Tests

[2] 10:15:00 - All checks complete!

=== Final Status ===
✅ Build and Test: pass
❌ E2E Tests: fail

Checks failed: E2E Tests. Not merging PR #318.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, the-waiting and version-check come with it.

Call it as `/release-ops:pr-wait`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **release-ops**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add release-ops@stylus-nexus
```

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, the-waiting and version-check come with it. In Codex, type `$` and the skill name (`$release-ops:pr-wait`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill pr-wait
```

Skills arrive without a pack prefix: `/pr-wait` in most agents and `@pr-wait` in Windsurf. opencode shows `/pr-wait` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/pr-wait .agents/skills/
```

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** Needs gh and your local repo.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No access to your local repo or git and gh credentials by default.

</details>
<!-- skill-readme:end -->
