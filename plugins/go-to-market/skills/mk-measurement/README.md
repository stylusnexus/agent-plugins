<!-- skill-readme:begin -->
# mk-measurement

This skill should be used when the user asks what to measure, whether marketing is working, how to set up a channel experiment, what belongs on a marketing dashboard, or how to read the results of a launch or campaign.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You cannot tell if your marketing works.

**Try:** `Build a scorecard for Plant Ledger and set up a test for the forum channel.`

**Skip it when:** You want ad-spend tuning inside an ad tool. This skill does not run campaigns.

## What it looks like

Example output, invented data (fictional product). Every metric sits on one funnel stage and has a formula you can recompute by hand.

| Stage | Metric | Formula | Source | Something's-wrong trigger | This period |
|---|---|---|---|---|---|
| Acquisition | waitlist sign-ups by channel | new sign-ups grouped by source tag | email tool | any channel drops 30% week on week | 118 |
| Activation | second-room rate | users with 2+ rooms ÷ sign-ups, 3-day window | product database | below 40% | 45% |
| Revenue | trial-to-paid | not yet applicable: pre-launch | none | none | none |

```text
EXPERIMENT CARD   Guided room setup vs. current setup
Primary metric    second-room rate     Sample size fixed in advance: 400 per arm
Decision rule     ship if +8 points or more; otherwise keep current setup
Checks            no early peeking; traffic split matches the 50/50 setting
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-measurement`, or let it start on its own when your request matches.

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

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-measurement`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-measurement
```

Skills arrive without a pack prefix: `/mk-measurement` in most agents and `@mk-measurement` in Windsurf. opencode shows `/mk-measurement` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-measurement .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-measurement` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-measurement.zip mk-measurement
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-measurement.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
