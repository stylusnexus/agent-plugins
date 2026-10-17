<!-- skill-readme:begin -->
# mk-audience

This skill should be used when the user asks who the first customer is, who to target, an ideal customer profile, buyer personas, who influences the buyer, where an audience gathers online, or how to segment customers.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex partial, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%97%90%20%C2%B7%20ChatGPT%20%E2%97%90-yellow)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: No audience-scout agent, so the verified-places step must be done inline with web search. Codex: Codex plugins do not carry agents, so audience-scout is missing and the verified-places step has no stated fallback. Other agents: The Skills CLI installs skills only, so audience-scout is missing and the verified-places step has no stated fallback.

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You do not know who your first customer is.

**Try:** `Who is the ideal customer for Plant Ledger? I have 6 interview notes and 14 sign-up forms.`

**Skip it when:** You already have a tested profile and need the words for it. Use mk-positioning or mk-copy.

## What it looks like

Example output, invented data (fictional product). Any field without a real source is marked, not filled with a guess.

```text
IDEAL CUSTOMER PROFILE                      Source
Who            hobby collector, 20+ indoor plants      14 beta sign-up forms
Already uses   phone calendar, a spreadsheet           6 interviews
Tried, quit    2 plant apps ("too many ads")           forum thread, 2026-08
Job (practical) keep every plant watered on time        interviews
Job (emotional) stop feeling guilty after a trip        3 interview quotes
Trigger        loses a plant after a holiday           MISSING INFORMATION
Disqualifier   owns fewer than 10 plants               ASSUMPTION
Segments       one for now; the evidence does not support a split by region
Buying roles   initiator and user are the same person; partner may share the app
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-audience`, or let it start on its own when your request matches.

**Note:** Uses the audience-scout agent that ships with the Claude Code plugin.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **go-to-market**. Plugins do not load in the app's cloud sessions.

**Note:** Uses the audience-scout agent that ships with the Claude Code plugin.

</details>

<details>
<summary>Codex (partial)</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add go-to-market@stylus-nexus
```

This installs the whole go-to-market pack, so marketing-lead, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-audience`), or run `/skills` to pick it.

**Limit:** Codex plugins do not carry agents, so audience-scout is missing and the verified-places step has no stated fallback.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-audience
```

Skills arrive without a pack prefix: `/mk-audience` in most agents and `@mk-audience` in Windsurf. opencode shows `/mk-audience` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** The Skills CLI installs skills only, so audience-scout is missing and the verified-places step has no stated fallback.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-audience .agents/skills/
```

**Limit:** The Skills CLI installs skills only, so audience-scout is missing and the verified-places step has no stated fallback.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-audience` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-audience.zip mk-audience
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-audience.zip`.

**Limit:** No audience-scout agent, so the verified-places step must be done inline with web search.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** No audience-scout agent, so the verified-places step must be done inline with web search.

</details>
<!-- skill-readme:end -->
