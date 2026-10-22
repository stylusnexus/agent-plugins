<!-- skill-readme:begin -->
# accessibility-review

Use when reviewing a UI for accessibility: keyboard operation, focus order and visibility, screen reader behavior, ARIA, accessible names and labels, forms and error messages, color contrast, reflow and zoom, target size, motion and reduced motion, status messages and live regions. Targets WCAG 2.2 AA in Next.js/React and Tailwind-style CSS. Produces prioritized findings with fixes and a list of checks that still need a browser or assistive technology.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Reviews code or screenshots you paste or upload; the source pass over a whole project needs the repo. The optional contrast script takes colours you type in.

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** You want a WCAG 2.2 AA review of keyboard, focus, names, contrast, forms or motion.

**Try:** `Review the Quill invoice form for accessibility.`

**Skip it when:** You want a compliance statement, a VPAT, or caption review. None of those can come from this skill.

## What it looks like

Example output, invented data (fictional product). Each finding is tagged VERIFIED (seen in source) or NEEDS-TEST (needs a browser or assistive technology).

```text
A1  Serious  WCAG 3.3.1 (A)   InvoiceForm.tsx:84
Observed    <input> for "Client email" has only a placeholder; error shown in red text
Affects     screen-reader users: the field has no accessible name, the error is not announced
Fix         <label htmlFor="email">Client email</label> and aria-describedby="email-error"
Evidence    VERIFIED (source)

A2  Moderate  WCAG 1.4.3 (AA)  tokens.css:12
Observed    #8a8a8a text on #ffffff measures 3.45:1 (needs 4.5:1)
Fix         use #767676 (4.54:1) or darker
Evidence    VERIFIED (computed)

Checks not performed: keyboard walk-through, 200% zoom, VoiceOver (no browser or device)
Summary     2 findings in the source pass. This is not a conformance statement.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it.

Call it as `/design-suite:accessibility-review`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:accessibility-review`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill accessibility-review
```

Skills arrive without a pack prefix: `/accessibility-review` in most agents and `@accessibility-review` in Windsurf. opencode shows `/accessibility-review` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** The optional contrast script needs Python 3.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/accessibility-review .agents/skills/
```

**Note:** The optional contrast script needs Python 3.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `accessibility-review` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r accessibility-review.zip accessibility-review
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `accessibility-review.zip`.

**Limit:** Reviews code or screenshots you paste or upload; the source pass over a whole project needs the repo. The optional contrast script takes colours you type in.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Reviews code or screenshots you paste or upload; the source pass over a whole project needs the repo. The optional contrast script takes colours you type in.

</details>
<!-- skill-readme:end -->
