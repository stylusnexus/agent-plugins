<!-- skill-readme:begin -->
# review-merge-pipeline

Automated pipeline that verifies changes with `prove-it`, code-reviews them, fixes issues found, commits, pushes, creates a PR, and merges when the user authorized it. Detects the repo's integration branch and branch rules rather than assuming them. Binds test and review evidence to the exact head commit and merges only on the real required-check status. Accepts an optional worktree path argument and flags --base / --no-prove / --no-review / --no-merge / --rebase / --cross-model. Use when work is done and you want to ship it without manual steps.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** Your work is done and you want review, fixes, a pull request and a merge in one run.

**Try:** `/review-merge-pipeline --no-merge`

**Skip it when:** You want to read the diff yourself before anything is committed or pushed.

## What it looks like

What happens to each review finding, by the reviewer's confidence:

| Confidence | Action |
|---|---|
| 90-100 (Critical) | Must fix before going further |
| 80-89 (Important) | Fix, unless it is a pre-existing pattern or out of scope |
| Below 80 (Minor) | Skip; note it in the PR description if relevant |

Example output, invented data.

```text
Running the review-merge pipeline.
...
Pipeline complete:
- PR: example-org/notes-app#233
- Status: Merged to dev
- Review: 3 issues found, 2 fixed (1 minor, noted in the PR)
- Base / head: dev@4e1a9c2 / 9b07d3f · merge commit 1c58e60
- Required checks: build, test passed for 9b07d3f · approval APPROVED
- N/A / UNVERIFIED: none
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:review-merge-pipeline`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:review-merge-pipeline`), or run `/skills` to pick it.

**Note:** Network steps need an approval; `--cross-model` from inside Codex adds no different-model view.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill review-merge-pipeline
```

Skills arrive without a pack prefix: `/review-merge-pipeline` in most agents and `@review-merge-pipeline` in Windsurf. opencode shows `/review-merge-pipeline` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** `--cross-model` needs the codex CLI.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/review-merge-pipeline .agents/skills/
```

**Note:** `--cross-model` needs the codex CLI.

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
