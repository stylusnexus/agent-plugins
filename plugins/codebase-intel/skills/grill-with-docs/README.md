<!-- skill-readme:begin -->
# grill-with-docs

Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise. Use when user wants to stress-test a plan against their project's language and documented decisions.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: The interview works; checking answers against code and updating the docs needs repo access.

Part of the [codebase-intel](../../README.md) pack.

## When and how to use it

**Use it when:** You have a plan and want it tested against your project's terms and past decisions.

**Try:** `Grill me on this plan to split Orders into Orders and Shipments. Update CONTEXT.md as we go.`

**Skip it when:** You only want a quick answer. This skill asks one question at a time.

## What it looks like

*Example exchange, invented data.*

> **Agent:** Your glossary defines **Cancellation** as ending a whole Order. This plan cancels one line item. Is that a Cancellation, or a new term? My recommendation: call it a **Line Removal**, and keep Cancellation for whole Orders.
>
> **You:** Line Removal. Cancellation stays whole-order.
>
> **Agent:** The code agrees: `cancelOrder()` only takes an order ID. Updating `CONTEXT.md` now. Next question: can a Line Removal happen after the Order has shipped?

```text
CONTEXT.md, added during the session:

**Line Removal**:
Taking one item off an Order before it ships. The Order stays open.
_Avoid_: Partial cancellation, item cancel
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install codebase-intel@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install codebase-intel@stylus-nexus` do the same. This installs the whole codebase-intel pack, so codebase-architecture-scanner, codebase-health, read-the-damn-docs and teach-code-to-mastery come with it.

Call it as `/codebase-intel:grill-with-docs`, or let it start on its own when your request matches.

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

This installs the whole codebase-intel pack, so codebase-architecture-scanner, codebase-health, read-the-damn-docs and teach-code-to-mastery come with it. In Codex, type `$` and the skill name (`$codebase-intel:grill-with-docs`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill grill-with-docs
```

Skills arrive without a pack prefix: `/grill-with-docs` in most agents and `@grill-with-docs` in Windsurf. opencode shows `/grill-with-docs` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/codebase-intel/skills/grill-with-docs .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `grill-with-docs` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/codebase-intel/skills
   zip -r grill-with-docs.zip grill-with-docs
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `grill-with-docs.zip`.

**Limit:** The interview works; checking answers against code and updating the docs needs repo access.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole codebase-intel pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** The interview works; checking answers against code and updating the docs needs repo access.

</details>
<!-- skill-readme:end -->
