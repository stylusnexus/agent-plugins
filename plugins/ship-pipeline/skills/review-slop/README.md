<!-- skill-readme:begin -->
# review-slop

This skill scans a branch diff before opening a PR for needless casts, unsupported abstractions, missing validation, misleading tests, and prose tells. Requires evidence and behavior-based repair criteria. Report-only, never fixes. Repo-agnostic; defers to a repo-local review-slop when one exists. Triggers on /review-slop and phrases like 'check this for slop', 'scan before the PR', 'does this read like AI wrote it'.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You finished a branch and want a list of weak spots before you open the pull request.

**Try:** `/review-slop`

**Skip it when:** You want the skill to fix the problems. It only reports them.

## What it looks like

Example output, invented data.

```text
Scanned: 9 files, origin/dev (a1b2c3d)...HEAD (e4f5a6b). Not scanned: 1 unstaged file.

HIGH
- Location: src/export/worker.ts:88
  What: cast to any on the job payload; ExportJob is one import away
  Why it matters: a renamed field still compiles and fails at runtime
  Suggested fix: type the payload as ExportJob (not applied)
  Evidence: ExportJob in src/export/types.ts:12; only caller queue.ts:40
  Acceptance: renaming ExportJob.pages breaks the typecheck

WARNING
- Location: docs/export.md:5
  What: "seamlessly handles any document", but exports stop at 500 pages
  Suggested fix: state the limit

Counts: CRITICAL 0 · HIGH 1 · WARNING 1
Open question: is the 500-page limit intended?
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:review-slop`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:review-slop`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill review-slop
```

Skills arrive without a pack prefix: `/review-slop` in most agents and `@review-slop` in Windsurf. opencode shows `/review-slop` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/review-slop .agents/skills/
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
