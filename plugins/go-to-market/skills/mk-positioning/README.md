<!-- skill-readme:begin -->
# mk-positioning

This skill should be used when the user asks for positioning, who a product is for and what it beats, why we win, a one-liner, a tagline, a messaging hierarchy, how to describe the product to a stranger, or what category to claim.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You cannot say in one line why your product beats the alternative.

**Try:** `Write the positioning for Plant Ledger. Buyers now use a phone calendar.`

**Skip it when:** Your positioning is settled and you need page copy. Use mk-copy.

## What it looks like

Example output, invented data (fictional product).

```text
1 Competitive alternative   a phone calendar with repeating reminders
2 Differentiated capability schedules per room that shift with season and travel
3 Value                     no plant lost to a reminder that fired on the wrong day
4 Target segment            collectors with 20+ plants in several rooms
5 Market category           watering tracker for collectors (not "plant care app")
Rejected                    "plant care app": puts us against plant-ID apps we don't beat
One-liner   Plant Ledger keeps a 40-plant collection on schedule, room by room,
            even when you travel.
Stakeholder check
  Customer   true and useful: yes        Business   supports a paid tier: unknown
  Community  names no competitor: yes
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-first-contact-audit, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach and mk-search come with it.

Call it as `/go-to-market:mk-positioning`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **go-to-market**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add go-to-market@stylus-nexus
```

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-first-contact-audit, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-positioning`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-positioning
```

Skills arrive without a pack prefix: `/mk-positioning` in most agents and `@mk-positioning` in Windsurf. opencode shows `/mk-positioning` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-positioning .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-positioning` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-positioning.zip mk-positioning
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-positioning.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
