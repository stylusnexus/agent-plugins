<!-- skill-readme:begin -->
# prove-it

End-of-work evidence protocol that proves a feature WORKS, not that checks pass. Repo-agnostic — discovers what CI actually gates (often far less than a green check implies), runs both static gates, targeted tests, terminus checks for threaded values, one real persistence round-trip, and render-surface verification, then emits a claim→command→result evidence table. Defers to a repo-local prove-it skill when one exists. Use before declaring any feature done and before shipping.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Runs in a remote sandbox without your local repo, git remotes or credentials. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You finished a feature and must show that it works before you call it done.

**Try:** `/prove-it`

**Skip it when:** The work is only docs or comments and has nothing to run.

## What it looks like

Example output, invented data.

```text
Running /prove-it verification.

| # | Claim                         | Command / location                     | Result      |
|---|-------------------------------|----------------------------------------|-------------|
| 1 | Types clean (baseline 3→3)    | npm run typecheck                      | PASS        |
| 2 | Build passes                  | npm run build                          | PASS        |
| 3 | New behavior tested           | export.test.ts (fails without the fix) | PASS        |
| 4 | Page count reaches the worker | worker.test.ts asserts pages = 120     | PASS        |
| 5 | Real write and read-back      | POST /api/export, then GET the file    | PASS        |
| 6 | Renders at /documents/[id]    | export.spec.ts, console clean          | PASS        |
| 7 | Works in mobile Safari        | —                                      | UNVERIFIED  |

7: no device available here; needs one run on a real phone.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it.

Call it as `/ship-pipeline:prove-it`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, review-merge-pipeline, review-slop, ship-issues, start-issue, stripe-billing and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:prove-it`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill prove-it
```

Skills arrive without a pack prefix: `/prove-it` in most agents and `@prove-it` in Windsurf. opencode shows `/prove-it` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/prove-it .agents/skills/
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
