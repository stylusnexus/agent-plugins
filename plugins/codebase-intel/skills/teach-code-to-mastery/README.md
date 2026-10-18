<!-- skill-readme:begin -->
# teach-code-to-mastery

Use when the user wants to DEEPLY understand code — a set of changes, a PR, a session of work, a tricky module, an algorithm, or a technical concept in the codebase — not just have it summarized. Teaches incrementally and gates progress on demonstrated mastery, using free-recall restatement and quizzes. Triggers on 'teach me X', 'help me understand X', 'quiz me on X', 'I want to really get X', 'walk me through what we built'. Single sitting, code only: not for exam or certification prep, and not for multi-session courses or books.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Teaching works on code you paste in; reading a diff, PR or repo needs repo access.

Part of the [codebase-intel](../../README.md) pack.

## When and how to use it

**Use it when:** You need to really understand a diff, PR, module or algorithm, not skim a summary.

**Try:** `Teach me what PR #412 changed. Don't move on until I can explain it.`

**Skip it when:** You only want a summary, or you are studying for an exam or working through a whole course or book.

## What it looks like

*Example exchange, invented data.*

```text
You:   Teach me what PR #412 did. I need to defend it in review.

Agent: Read the diff and the two files it touches. First, in your own words:
       why was the old retry loop making outages worse?

You:   It retried too slowly.

Agent: Not quite, and that is the part worth fixing. Every client retried on
       the same schedule, so they all hit the upstream together. (client.ts:88)
       Quick check - which of these is the problem?
       [ ] Retries were too slow
       [ ] Retries were synchronized
       [ ] Retries had no cap
       Checklist: problem 0/3 verified. Solution and context not started.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install codebase-intel@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install codebase-intel@stylus-nexus` do the same. This installs the whole codebase-intel pack, so codebase-architecture-scanner, codebase-health, grill-with-docs and read-the-damn-docs come with it.

Call it as `/codebase-intel:teach-code-to-mastery`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **codebase-intel**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add codebase-intel@stylus-nexus
```

This installs the whole codebase-intel pack, so codebase-architecture-scanner, codebase-health, grill-with-docs and read-the-damn-docs come with it. In Codex, type `$` and the skill name (`$codebase-intel:teach-code-to-mastery`), or run `/skills` to pick it.

**Note:** Multiple-choice quizzes become plain-text questions where the host has no structured question tool.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill teach-code-to-mastery
```

Skills arrive without a pack prefix: `/teach-code-to-mastery` in most agents and `@teach-code-to-mastery` in Windsurf. opencode shows `/teach-code-to-mastery` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/codebase-intel/skills/teach-code-to-mastery .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `teach-code-to-mastery` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/codebase-intel/skills
   zip -r teach-code-to-mastery.zip teach-code-to-mastery
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `teach-code-to-mastery.zip`.

**Limit:** Teaching works on code you paste in; reading a diff, PR or repo needs repo access.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole codebase-intel pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Teaching works on code you paste in; reading a diff, PR or repo needs repo access.

</details>
<!-- skill-readme:end -->
