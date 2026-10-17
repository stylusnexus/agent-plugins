<!-- skill-readme:begin -->
# db-truth

Ground every database claim in the live database. Repo-agnostic — pre-work verification before any spec, plan, or code that touches tables (schema shape, M2M vs scalar, RLS/permissions, function properties), and post-apply verification that migrations actually landed (ledger, object existence, type regen). Defers to a repo-local db-truth skill when one exists. Use BEFORE designing anything DB-touching and AFTER every migration apply.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** A spec or plan touches database tables and you have not looked at the live schema.

**Try:** `/db-truth pre-work for the invoices and payments tables`

**Skip it when:** The change touches no database.

## What it looks like

Example exchange, invented data.

```text
> /db-truth pre-work   (before planning a "project owner" badge)

Running /db-truth pre-work verification.
Live schema:
  projects:        id uuid, name text, created_at timestamp     (no owner column)
  project_members: project_id uuid, user_id uuid, role text
Relationships:
  project ↔ user: M2M through project_members, not a scalar owner_id
Permissions: project_members has no INSERT policy for the new role
Call site named in the plan: src/projects/badge.ts:41 (confirmed by grep)
Verdict: the spec's "project.owner_id" does not exist. Stopping.
Revise the data model to read role = 'owner' from project_members.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:db-truth`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:db-truth`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill db-truth
```

Skills arrive without a pack prefix: `/db-truth` in most agents and `@db-truth` in Windsurf. opencode shows `/db-truth` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/db-truth .agents/skills/
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
