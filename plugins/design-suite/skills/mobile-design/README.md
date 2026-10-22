<!-- skill-readme:begin -->
# mobile-design

Use when designing or reviewing mobile, responsive or small-screen interfaces: touch targets, thumb reach, bottom bar or drawer navigation, back behaviour, gestures, mobile forms and keyboards, viewport and safe-area handling, slow or offline networks, layout shift, reduced motion. Also for deciding whether a responsive web experience is enough versus a native app.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** A flow must work on phones, or a desktop layout needs to adapt to narrow widths.

**Try:** `Adapt the Quill invoice list and send flow for phones.`

**Skip it when:** The question is about desktop-only layout, or you want a native app built.

## What it looks like

Example output, invented data (fictional product). Device mix and connectivity are unknown, so they are marked.

```text
Screen: Invoice list         Device mix: MISSING INFORMATION
Priority    1 status + amount   2 client   3 due date   (actions in a row menu)
Layout      narrow: single column cards   medium: two-line rows   wide: table
Controls    Send button 48 px high (recommended); row menu target 44 x 44 px
Navigation  bottom bar with 3 items; back returns to the list with filters kept
States      empty, loading, offline ("Will send when you are back online"), error
Input       client email field: type=email, autocomplete=email
Accept      at 320 CSS px wide and 200% text size, nothing scrolls sideways
Web or native   responsive web is enough for this flow (product owners decide)
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, dashboard-design, information-architecture, interface-polish and ui-ux come with it.

Call it as `/design-suite:mobile-design`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **design-suite**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add design-suite@stylus-nexus
```

This installs the whole design-suite pack, so accessibility-review, dashboard-design, information-architecture, interface-polish and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:mobile-design`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mobile-design
```

Skills arrive without a pack prefix: `/mobile-design` in most agents and `@mobile-design` in Windsurf. opencode shows `/mobile-design` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/mobile-design .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mobile-design` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r mobile-design.zip mobile-design
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mobile-design.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
