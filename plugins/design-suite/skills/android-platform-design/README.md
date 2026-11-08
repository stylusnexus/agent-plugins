<!-- skill-readme:begin -->
# android-platform-design

Use when designing or reviewing an interface for Android and Google platforms against Material Design 3 and the Android developer docs: navigation bar, rail and drawer, edge-to-edge and window insets, predictive back, adaptive layouts and window size classes for phones, tablets and foldables, dynamic color, 48dp touch targets, TalkBack, system font scaling, snackbars, permissions.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** A screen ships on Android phones, tablets or foldables and should follow Material 3 and platform behaviour.

**Try:** `Review the Quill invoice list on Android across phone and tablet widths.`

**Skip it when:** The question is platform-neutral (use mobile-design), needs exact contrast ratios or screen-reader testing (use accessibility-review), or is about Apple platforms.

## What it looks like

Example output, invented data (fictional product). This is expert review from source and screenshots, not a device test.

```text
Expert review against Material Design 3 and Android developer guidance, versions assumed: MISSING INFORMATION
Screen: Invoice list     Window classes: compact, medium

A1  high    Adaptive     Bottom bar is kept at medium width, with a stretched single column
            Fix          navigation rail at medium; list-detail layout
A2  high    Edge-to-edge Send button sits under the gesture bar on the invoice form
            Fix          apply system bar and keyboard insets to the bottom action area
A3  medium  Back         Back press is intercepted with the old back method, so no preview shows
            Fix          use the back callback API; ask before discarding a draft
A4  medium  Targets      Row menu icon is 32dp with no padding
            Fix          48dp touch target around the icon
Evidence    all four VERIFIED from source; none run on a device

Checks not performed: device or emulator run, TalkBack, largest font scale, foldable, three-button navigation, Play policy
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, apple-platform-design, art-direction, dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it.

Call it as `/design-suite:android-platform-design`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so accessibility-review, apple-platform-design, art-direction, dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:android-platform-design`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill android-platform-design
```

Skills arrive without a pack prefix: `/android-platform-design` in most agents and `@android-platform-design` in Windsurf. opencode shows `/android-platform-design` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/android-platform-design .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `android-platform-design` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r android-platform-design.zip android-platform-design
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `android-platform-design.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
