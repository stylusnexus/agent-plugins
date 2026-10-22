<!-- skill-readme:begin -->
# ui-ux

Use when the user asks to design, review, critique or improve a product interface, user flow, screen states, error handling, navigation, layout, or interaction, or wants a design brief or a handoff to implementation. Entry point for the design suite: frames the user task, then routes to dashboard, mobile, information-architecture, accessibility or implementation roles.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** You are designing or reviewing a flow, screen or state and want a brief before anyone builds.

**Try:** `Review the Quill "send invoice" flow and write a design brief.`

**Skip it when:** The question is only about one area, such as navigation labels or contrast. Use the matching skill.

## What it looks like

Example output, invented data (fictional product). This is an expert heuristic review, not user research.

```text
BRIEF: Send invoice                       Evidence: code + 3 screenshots supplied
User and task   freelancer sends a finished invoice to a client in under a minute
Unknown         how often clients ask for a resend (MISSING INFORMATION)

Finding                                           Kind            Severity
Send button looks the same when disabled           observation     high
No state shown while the email is sending          observation     high
Users may think "Send" also marks it paid          interpretation  medium (test it)
Add a sending state and a "Sent to ana@example.com" confirmation   recommendation

Acceptance criteria
- Send is disabled with a stated reason until a client email is set
- A sending, sent and failed state each exist, and failed offers Retry
Needs real users: does "Send" read as "mark paid"? Run a five-person test.
```

## Install

This skill reads shared files in its sibling skills, so install the whole design-suite pack. The Claude Code and Codex plugins do that already; with the Skills CLI or a folder copy, take every skill in the pack.

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, dashboard-design, information-architecture, interface-polish and mobile-design come with it.

Call it as `/design-suite:ui-ux`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so accessibility-review, dashboard-design, information-architecture, interface-polish and mobile-design come with it. In Codex, type `$` and the skill name (`$design-suite:ui-ux`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

This skill reads shared files in its sibling skills, so install every skill in the pack:

```bash
npx skills add stylusnexus/agent-plugins --skill accessibility-review dashboard-design information-architecture interface-polish mobile-design ui-ux
```

Skills arrive without a pack prefix: `/ui-ux` in most agents and `@ui-ux` in Windsurf. opencode shows `/ui-ux` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Install the whole pack: this skill routes to its sibling skills.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy every skill in the pack, so the shared files sit beside this one:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/. .agents/skills/
```

**Note:** Install the whole pack: this skill routes to its sibling skills.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `ui-ux` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r ui-ux.zip ui-ux
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `ui-ux.zip`.

**Note:** Routing to the sibling skills and design agents needs the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
