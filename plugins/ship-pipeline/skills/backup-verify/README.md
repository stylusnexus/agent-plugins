<!-- skill-readme:begin -->
# backup-verify

Confirm database backups exist AND actually restore, by enumerating Neon branch snapshots / Supabase scheduled backups / pg_dump artifacts, restoring into a scratch branch, running smoke queries, and recording timestamped evidence. Use before any risky migration or production mutation, and on a monthly cadence regardless.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You are about to run a risky migration and need proof that a backup restores.

**Try:** `Run a backup restore drill before the orders migration`

**Skip it when:** You only want to know whether backups are switched on. This skill restores them.

## What it looks like

Example output, invented data.

```text
Backup mechanism: Neon point-in-time restore plus snapshots
Backup used: snapshot snap-0412, taken 2026-10-14 03:00 UTC
Restore drill: 2026-10-14 09:20 UTC into branch backup-drill-20261014
  neon snapshots restore snap-0412 --name backup-drill-20261014

Row counts      restored   live now
  User            18,204     18,231
  Subscription     4,112      4,115
  Customer         4,090      4,093
Newest Subscription row: 02:58 UTC (just before the backup)
Orphaned subscriptions: 0
Differences match writes made after 03:00 UTC.

Result: PASS. Scratch branch deleted.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:backup-verify`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:backup-verify`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill backup-verify
```

Skills arrive without a pack prefix: `/backup-verify` in most agents and `@backup-verify` in Windsurf. opencode shows `/backup-verify` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/backup-verify .agents/skills/
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
