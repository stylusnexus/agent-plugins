<!-- skill-readme:begin -->
# apple-platform-design

Use when designing or reviewing an interface for Apple platforms (iOS, iPadOS, macOS, watchOS) against the Human Interface Guidelines: tab bars, navigation stacks, sheets and alerts, SF Symbols, Dynamic Type, safe areas, system gestures, haptics, iPad multitasking and sidebars, macOS menu bar, windows and keyboard shortcuts, watchOS glanceable screens, VoiceOver and Reduce Motion handling, dark mode.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** A screen ships on iPhone, iPad, Mac or Apple Watch and should feel native.

**Try:** `Review the Quill invoice list for iPhone and iPad against the Human Interface Guidelines.`

**Skip it when:** The question is platform-neutral (use mobile-design), needs exact contrast ratios or screen-reader testing (use accessibility-review), or is about Android.

## What it looks like

Example output, invented data (fictional product). This is expert review from source and screenshots, not a device test.

```text
Expert review against Apple Human Interface Guidelines, OS assumed: MISSING INFORMATION
Screen: Invoice list     Platforms: iPhone, iPad

H1  high    Navigation   Hamburger menu holds all five sections
            Fix          tab bar with Invoices, Clients, Reports, Settings; sidebar on iPad
H2  high    Dynamic Type Amount and status sit in one row with a fixed 44 pt height
            Fix          text styles, and stack the row at accessibility sizes
H3  medium  Sheets       "New invoice" sheet closes on swipe-down and drops typed data
            Fix          ask before discarding (Discard, Keep Editing)
H4  medium  Gestures     Delete is available only as a swipe action
            Fix          add Delete to the row's context menu and the detail screen
Evidence    all four VERIFIED from source; none run on a device

Checks not performed: device or simulator run, VoiceOver, largest text size, Reduce Motion, iPad Split View, App Review
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, android-platform-design, art-direction, dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it.

Call it as `/design-suite:apple-platform-design`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so accessibility-review, android-platform-design, art-direction, dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:apple-platform-design`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill apple-platform-design
```

Skills arrive without a pack prefix: `/apple-platform-design` in most agents and `@apple-platform-design` in Windsurf. opencode shows `/apple-platform-design` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/apple-platform-design .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `apple-platform-design` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r apple-platform-design.zip apple-platform-design
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `apple-platform-design.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
