<!-- skill-readme:begin -->
# dashboard-design

Use when designing, reviewing or fixing a dashboard, internal console, operations or status view, metrics page, KPI summary, chart or data table, or any data-heavy screen. Covers decision-first layout, freshness and provenance, missing/stale/partial data states, alert thresholds, number and chart choices, and review findings.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** A dashboard is noisy, looks healthy when it should not, or is being designed from scratch.

**Try:** `Design the Quill revenue overview for a freelancer who checks it each Monday.`

**Skip it when:** You only need a chart type for one number. Ask directly.

## What it looks like

Example output, invented data (fictional product). Thresholds are labelled recommended and need owner confirmation.

```text
User and decision   freelancer, weekly: "who do I chase this week?"   (cadence: assumption)
Layout by priority  1 overdue invoices (count, total, oldest)   2 due this week   3 paid this month

Signal             Source             Freshness     States designed
Overdue total      invoices table     live          loading, empty ("nothing overdue"), error
Bank sync          bank provider      checked 09:12 stale after 24 h (recommended), unavailable
"All clear" shows only when the bank sync is fresh. Otherwise: "Bank not checked since 09:12".
Open question   which overdue age should turn red? (owner decision)
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, information-architecture, interface-polish, mobile-design and ui-ux come with it.

Call it as `/design-suite:dashboard-design`, or let it start on its own when your request matches.

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

This installs the whole design-suite pack, so accessibility-review, information-architecture, interface-polish, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:dashboard-design`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill dashboard-design
```

Skills arrive without a pack prefix: `/dashboard-design` in most agents and `@dashboard-design` in Windsurf. opencode shows `/dashboard-design` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/dashboard-design .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `dashboard-design` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r dashboard-design.zip dashboard-design
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `dashboard-design.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
