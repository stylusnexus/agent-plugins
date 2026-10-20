<!-- skill-readme:begin -->
# the-waiting

Use while waiting on CI, a deploy, or a release run and you want to know how long is really left. Estimates each running job's finish from its own recent history, spots runs stuck behind a cancelled run that never stopped, and suggests a few small tasks for the meantime. Report-only; never cancels, reruns, or merges. Triggers on /the-waiting and phrases like 'how long is CI going to take', 'why is this still pending', 'what's the hold-up', 'the waiting is the hardest part'.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** CI has been pending for a while and you want to know how long is left.

**Try:** `/the-waiting 318`

**Skip it when:** You want to cancel, rerun or merge. This skill only reports.

## What it looks like

Example output, invented data.

```text
Unit Tests (full suite): 18m elapsed, usually 26m (p90 31m, 14 runs) → ~8m left.
Lint: 2m elapsed, usually 3m (p90 4m, only 4 runs, so rough) → ~1m left.
Type Check: done ✓.  Nothing stuck.

Sound check is running long; the drummer is still looking for his sticks.

Meantime, each under five minutes:
  - PR #233 is waiting on your review
  - your PR #229 has a stale lint check
  - issue #241 (typo on the settings page) is assigned to you
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, version-check and vscode-marketplace-publish come with it.

Call it as `/release-ops:the-waiting`, or let it start on its own when your request matches.

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

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, llm-cost-audit, npm-publish, observability-setup, pr-wait, version-check and vscode-marketplace-publish come with it. In Codex, type `$` and the skill name (`$release-ops:the-waiting`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill the-waiting
```

Skills arrive without a pack prefix: `/the-waiting` in most agents and `@the-waiting` in Windsurf. opencode shows `/the-waiting` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/the-waiting .agents/skills/
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
