<!-- skill-readme:begin -->
# plan-arbiter

Use when asked to compare, cross-review, merge, judge, choose, or arbitrate competing plans from multiple agents such as Codex and Claude Code; when given two or more proposed plans, session IDs, transcripts, plan documents, PR descriptions, or pasted strategies; or when the user wants one recommended execution plan after agents review each other's proposals.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Compares pasted plans; their claims stay unverified without repo access.

Part of the [second-opinion](../../README.md) pack.

## When and how to use it

**Use it when:** Two or more agents wrote competing plans and you need one plan.

**Try:** `Compare these two plans for the checkout fix and give me one plan to run.`

**Skip it when:** You have one plan and only want it checked against the code. Use `spec-review`.

## What it looks like

*Example output, invented data.*

```text
| Tie-break order          | Plan A                   | Plan B                          |
| 1 Fits the request       | yes                      | yes, plus an admin UI not asked |
| 2 Grounded in real code  | names real files         | assumes a job queue that is not there |
| 3 Simpler first step     | one migration            | two new services                |
| 4 Validation, rollback   | no rollback story        | feature flag and backfill test  |
| 5 Execution cost         | low                      | medium                          |

Decision      Hybrid
Why           A is grounded and simpler; B has the better rollback path.
Execution     1 migration  2 service change behind a flag  3 backfill  4 remove flag
Borrowed      B's feature flag and backfill dry run
Rejected      B's admin UI (not requested); B's job queue (does not exist)
Verification  migration test, backfill dry run, CI green
Executor      a cheaper coding model: the plan is concrete and bounded
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install second-opinion@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install second-opinion@stylus-nexus` do the same. This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, efficient-frontier-routing, llm-council and spec-review come with it.

Call it as `/second-opinion:plan-arbiter`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **second-opinion**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, efficient-frontier-routing, llm-council and spec-review come with it. In Codex, type `$` and the skill name (`$second-opinion:plan-arbiter`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill plan-arbiter
```

Skills arrive without a pack prefix: `/plan-arbiter` in most agents and `@plan-arbiter` in Windsurf. opencode shows `/plan-arbiter` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/second-opinion/skills/plan-arbiter .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `plan-arbiter` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/second-opinion/skills
   zip -r plan-arbiter.zip plan-arbiter
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `plan-arbiter.zip`.

**Limit:** Compares pasted plans; their claims stay unverified without repo access.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole second-opinion pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Compares pasted plans; their claims stay unverified without repo access.

</details>
<!-- skill-readme:end -->

## /plan-arbiter

Compare competing agent plans and choose one executable direction.

`/plan-arbiter` is for workflows where two or more agents, often Codex and
Claude Code, each produce a plan and then need a judge to cross-review,
reconcile, and pick what should actually be implemented.

## What It Does

- Collects plans from pasted text, files, sessions, transcripts, PRs, comments,
  or plan links.
- Normalizes each plan into assumptions, scope, files, sequence, and
  verification.
- Reviews plans against each other and against the real task context.
- Chooses a winner, creates a hybrid, or sends the plans back for revision.
- Produces one implementation handoff with rejected alternatives and validation
  gates.

## When To Use It

Use it when a user says things like:

- "Have Codex and Claude each make a plan, then choose one."
- "Review these two plans against each other."
- "Merge the best parts and tell me which agent should execute."
- "Pick the cheaper execution path if quality is comparable."

Skip it when there is only one straightforward plan and no meaningful
alternative to evaluate.

## Output

The skill returns a short decision memo: decision, why, execution plan, borrowed
pieces, rejected ideas, verification, and executor recommendation.
