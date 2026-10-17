<!-- skill-readme:begin -->
# start-issue

Issue intake ritual before starting any work on a GitHub issue. Repo-agnostic — reads the full issue (body + comments), verifies the work isn't already shipped, checks premises against live code, captures a baseline, and creates a correctly-named branch off the integration branch. Defers to a repo-local start-issue skill when one exists. Usage: /start-issue <issue-number>

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You are about to work on a GitHub issue and want to check its scope, status and branch first.

**Try:** `/start-issue 412`

**Skip it when:** The issue is a trivial typo fix and you already know the scope.

## What it looks like

Example output, invented data.

```text
Running /start-issue intake for #412.

INTAKE #412 — PDF export fails for long documents
Goal: export succeeds for documents of any length
In scope: export payload limit   Out of scope: export styling (#398)
Done when: a 120-page document exports; a real failure shows an error
Already-shipped check: searched PRs and issues for "412" and "export"; nothing merged. Not shipped.
Premise check: issue is fresh (4 days old); the 30-page limit is still in the code
Branch: fix/412-long-pdf-export   Baseline: 3 typecheck errors
DB touched: no
Test cases (plain English):
  - a 5-page document still exports
  - a 120-page document exports
  - a failed export shows an error instead of doing nothing
Plan next: inline plan
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:start-issue`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **ship-pipeline**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:start-issue`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill start-issue
```

Skills arrive without a pack prefix: `/start-issue` in most agents and `@start-issue` in Windsurf. opencode shows `/start-issue` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/start-issue .agents/skills/
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
