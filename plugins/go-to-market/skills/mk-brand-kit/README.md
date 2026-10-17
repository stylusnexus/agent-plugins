<!-- skill-readme:begin -->
# mk-brand-kit

This skill should be used when the user asks for a brand kit, product voice, a palette, fonts, a logo system, visual consistency, brand guidelines, or which design tool to use for a marketing asset.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** Your colors and fonts differ from page to page.

**Try:** `Make a brand kit for Plant Ledger and check the text contrast.`

**Skip it when:** You need the words on a page. Use mk-copy.

## What it looks like

Example output, invented data (fictional product). Colors are exact values, and each pairing has a measured WCAG contrast ratio.

| Role | Hex | Paired against | Contrast | Passes? |
|---|---|---|---|---|
| Body text | #1F2A24 | background #F7F5EF | 13.61:1 | yes (4.5:1 normal text) |
| Accent text, links | #2E6B4F | background #F7F5EF | 5.78:1 | yes |
| Button label | #FFFFFF | button #2E6B4F | 6.30:1 | yes |
| Decorative leaf | #8FBF9F | background #F7F5EF | 1.90:1 | no: never use it for text |

Type roles: heading and body only, from one font family. The product voice sheet is marked HUMAN DECISION REQUIRED until the owner approves it.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-brand-kit`, or let it start on its own when your request matches.

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

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-brand-kit`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-brand-kit
```

Skills arrive without a pack prefix: `/mk-brand-kit` in most agents and `@mk-brand-kit` in Windsurf. opencode shows `/mk-brand-kit` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-brand-kit .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-brand-kit` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-brand-kit.zip mk-brand-kit
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-brand-kit.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
