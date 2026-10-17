<!-- skill-readme:begin -->
# db-migration-safety

Write or review Prisma and Supabase database migrations safely using the expand-contract pattern, idempotent SQL, and batched backfills. Use when adding/changing columns or tables, writing a migration PR, or reviewing one before merge — especially against Neon Postgres or Supabase in production.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Writes and reviews migration SQL from pasted text; the backup gate and branch test cannot run.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You are adding a column or table to a live database and want the change split into safe steps.

**Try:** `Review this migration that adds a NOT NULL column to the orders table`

**Skip it when:** The change is only a seed script or a brand new empty table in a dev database.

## What it looks like

Each phase is its own migration and its own deploy:

| Phase | What ships | Old code still works? |
|---|---|---|
| 1. Expand | New column or table, nullable or with a default, additive only | Yes |
| 2. Backfill | Existing rows filled in small batches, alongside live traffic | Yes |
| 3. Migrate reads and writes | App code writes to, then reads from, the new shape | Both shapes coexist briefly |
| 4. Contract | Drop the old column, add `NOT NULL`, once the backfill is confirmed | Only after every instance runs the new code |

Collapsing phases 1 and 4 into one migration is the most common cause of an avoidable outage. Phase 4 waits for a confirmed backup from `backup-verify`.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:db-migration-safety`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:db-migration-safety`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill db-migration-safety
```

Skills arrive without a pack prefix: `/db-migration-safety` in most agents and `@db-migration-safety` in Windsurf. opencode shows `/db-migration-safety` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/db-migration-safety .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `db-migration-safety` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/ship-pipeline/skills
   zip -r db-migration-safety.zip db-migration-safety
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `db-migration-safety.zip`.

**Limit:** Writes and reviews migration SQL from pasted text; the backup gate and branch test cannot run.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole ship-pipeline pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Writes and reviews migration SQL from pasted text; the backup gate and branch test cannot run.

</details>
<!-- skill-readme:end -->
