<!-- skill-readme:begin -->
# deploy

Promote the integration branch to production as one authorized batch. Repo-agnostic — detects the repo's branch names, merge strategy, and release tooling from its own history, and defers to any repo-local runbook. Freezes the source commit, proves the live artifact matches it, records migration, publish, smoke, and rollback evidence, and closes only issues proved shipped. Use when ready to push to production.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** The integration branch is ready and you have decided to promote it to production.

**Try:** `/deploy`

**Skip it when:** The work is not yet merged to the integration branch, or the repo ships from a single branch with nothing to promote.

## What it looks like

After a squash deploy, the file diff can show work that already shipped. The skill reads both signals together:

| File diff | New commit list | Read it as |
|---|---|---|
| Tiny | Huge | Phantom diff; trust the file diff |
| Huge | Tiny | Trust the commit list; the PR title describes only those commits |
| Large | Large | Genuinely large |
| Small or empty | Small or empty | Minimal; abort if there is nothing |

Example output, invented data.

```text
Deploy complete:
- Repo / PR: example-org/notes-app #240
- Files changed: 14 (+412/-96)
- Version: 2.8.0
- Publishes: none
- Migrations: applied 20261014_add_export_jobs (additive; backup verified 2026-10-14 09:12Z)
- Host: auto-deploys from main
- Batch: #231 export jobs, #236 export retry
- Source: 7d2f1e0 · previous source 3a9c4b8
- Artifact: release commit 5e60b21 · live 5e60b21 (matches)
- Checks: build, test passed for 7d2f1e0 · approval APPROVED
- Smoke: health ok · auth read ok · export page ok · write + read-back ok · errors for 5 min: none new
- Rollback: not needed
- Issues: closed #231, #236 · candidates not closed: #229 (bare mention, not a closing keyword)
- Back-merge: clean
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

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:deploy`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:deploy`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill deploy
```

Skills arrive without a pack prefix: `/deploy` in most agents and `@deploy` in Windsurf. opencode shows `/deploy` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/deploy .agents/skills/
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
