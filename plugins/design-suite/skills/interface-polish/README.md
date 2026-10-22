<!-- skill-readme:begin -->
# interface-polish

Use when polishing or reviewing the visual details of a UI: spacing and layout rhythm, border radii, shadows and borders, typography, colour tokens, dark mode, motion and transitions, interaction states (hover, focus, active, disabled, loading, empty, error), form visuals, and responsive layout. Written for Next.js/React with Tailwind-style utility CSS.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Reviews code or screenshots you paste or upload; the source pass over a whole project needs the repo. The optional scan script needs a local checkout.

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** A screen works but spacing, radii, type, colour or motion feel inconsistent.

**Try:** `Polish the Quill invoice list. Report only; do not edit files.`

**Skip it when:** You need exact contrast ratios or screen-reader behaviour (use accessibility-review), or a full redesign (use ui-ux).

## What it looks like

Example output, invented data (fictional product). The report uses the project's own tokens, and nothing here was verified in a browser.

```text
Mode: report only          Design system used: tailwind.config.ts

Principle        Before                              After                      File
Spacing scale    gap-[13px] between rows            gap-3 (token)              InvoiceList.tsx
Transitions      transition: all 300ms              transition-colors 150ms    Row.tsx
Radius           card rounded-lg inside rounded-lg  inner rounded-md            Card.tsx

Not fixed
Severity  Finding                                           File
medium    Empty list shows a blank area, no empty state     InvoiceList.tsx

Could not verify: dark mode and 320px width (no browser available)
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, art-direction, dashboard-design, information-architecture, mobile-design and ui-ux come with it.

Call it as `/design-suite:interface-polish`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so accessibility-review, art-direction, dashboard-design, information-architecture, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:interface-polish`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill interface-polish
```

Skills arrive without a pack prefix: `/interface-polish` in most agents and `@interface-polish` in Windsurf. opencode shows `/interface-polish` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** The optional scan script needs Python 3.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/interface-polish .agents/skills/
```

**Note:** The optional scan script needs Python 3.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `interface-polish` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r interface-polish.zip interface-polish
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `interface-polish.zip`.

**Limit:** Reviews code or screenshots you paste or upload; the source pass over a whole project needs the repo. The optional scan script needs a local checkout.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Reviews code or screenshots you paste or upload; the source pass over a whole project needs the repo. The optional scan script needs a local checkout.

</details>
<!-- skill-readme:end -->
