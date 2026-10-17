<!-- skill-readme:begin -->
# ship-issues

Take a batch of GitHub issues from intake through merge — and, only for a ship/deploy/release request, on through a production deploy and validation. 'Ship' means deploying to production: for that request it grounds every issue, reports status and grouping before any edit, implements each group, merges, deploys, and validates against production, calling start-issue, prove-it, review-merge-pipeline and deploy rather than restating them. An 'implement and merge' request stops after the merges — no promotion, no deploy. Repo-agnostic; defers to a repo-local ship-issues when one exists. Use on /ship-issues <N> <N> ..., or when asked to implement and ship/deploy/release several issues (deploys), or to implement and merge them (does not deploy).

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default. Other agents: Needs subagents for specialist review and parallel work; documented for Cursor, Gemini CLI/Antigravity CLI and opencode, not for Copilot, Windsurf or Cline.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You have a batch of related issues and want them taken from intake to merge, or to production.

**Try:** `Implement and merge issues 101, 204 and 317 with /ship-issues. Do not deploy.`

**Skip it when:** You have one small issue. Run start-issue, then prove-it and review-merge-pipeline.

## What it looks like

Example output, invented data.

```text
Running /ship-issues for #412, #415, #420.

Base: dev = 7c1e9a0, main = 3b4d2f8 (verified via gh). Unreleased on dev: yes, 2 PRs.
Goes live on merge? no — the host deploys from main only (render.yaml)
| Issue | Status         | What's left                           |
| #412  | Open work      | everything                            |
| #415  | Partly shipped | PR #402 added the API; the UI is left |
| #420  | Shipped        | PR #398 on main, checked live         |
Groups: export → #412, #415 → fix/412-export-limits
Dependencies / blocked: none
Decisions needing consultation: should the page limit be per plan?
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:ship-issues`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:ship-issues`), or run `/skills` to pick it.

**Note:** Network steps need an approval; subagent steps use Codex subagents.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill ship-issues
```

Skills arrive without a pack prefix: `/ship-issues` in most agents and `@ship-issues` in Windsurf. opencode shows `/ship-issues` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Needs subagents for specialist review and parallel work; documented for Cursor, Gemini CLI/Antigravity CLI and opencode, not for Copilot, Windsurf or Cline.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/ship-issues .agents/skills/
```

**Limit:** Needs subagents for specialist review and parallel work; documented for Cursor, Gemini CLI/Antigravity CLI and opencode, not for Copilot, Windsurf or Cline.

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
