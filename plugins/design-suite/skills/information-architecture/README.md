<!-- skill-readme:begin -->
# information-architecture

Use when the user asks to organize product or site content, navigation, menus, labels, taxonomy, categories, facets, URL structure, content types, redirects, or findability. Covers hierarchy and navigation models, naming rules, taxonomy design, findability checks (tree tests, card sorts as plans, scenario walkthroughs), and URL and content-model structure.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** Navigation, labels or URLs are being reorganised, or people cannot find something.

**Try:** `Reorganise the Quill settings menu; people cannot find tax settings.`

**Skip it when:** You want visual styling for the menu. Use interface-polish.

## What it looks like

Example output, invented data (fictional product). The walkthrough is expert review, not a tree-test result.

```text
Settings
  Account         profile, password, email
  Billing         plan, payment method
  Invoicing       numbering, due dates, tax rates   <- moved from "Advanced"
  Integrations    bank sync, calendar

Current label  Proposed label   Reason
Advanced       Invoicing        "Advanced" says nothing; tax and numbering live here
Task path      "Add VAT rate": Settings > Invoicing > Tax rates (3 steps)
Redirect       /settings/advanced -> /settings/invoicing (proposal, not applied)
Needs real users: a 5-participant tree test of the new labels. Results: MISSING INFORMATION.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, dashboard-design, interface-polish, mobile-design and ui-ux come with it.

Call it as `/design-suite:information-architecture`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so accessibility-review, dashboard-design, interface-polish, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:information-architecture`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill information-architecture
```

Skills arrive without a pack prefix: `/information-architecture` in most agents and `@information-architecture` in Windsurf. opencode shows `/information-architecture` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/information-architecture .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `information-architecture` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r information-architecture.zip information-architecture
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `information-architecture.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
