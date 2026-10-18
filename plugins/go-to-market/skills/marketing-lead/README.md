<!-- skill-readme:begin -->
# marketing-lead

This skill should be used when the user asks for a marketing lead, marketing help, a marketing plan, a campaign, how to market or promote a product, why nobody is using it, go-to-market execution, getting users or customers, or teaching marketing while doing it — for any product or project the user is building.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You have a product, a few hours a week, and no marketing plan.

**Try:** `Help me plan marketing for Plant Ledger. I have 4 hours a week and 35 waitlist sign-ups.`

**Skip it when:** You only need one focused answer, such as a positioning line. Use the matching mk skill.

## What it looks like

Example output, invented data (fictional product).

```text
PLAN: next 6 weeks                         Hours available: 4 a week
Goal         200 collectors on the waitlist by week 6 (now: 35)
Who acts     collectors with 20+ plants who lose plants while traveling
What moves   seeing their own rooms on a schedule in under 2 minutes
Channels     1. one collector forum, 2 h/week   stop if under 10 sign-ups by week 3
             2. founder posts, 1 h/week         stop if under 5 sign-ups by week 4
             3. waitlist email, 1 h/week        check replies, not opens
Not doing    paid ads (no budget), press (nothing to show yet)
Decided      collectors first; casual owners later
Open         does "travel mode" matter more than room setup? (assumption)
Next action  today: write the forum intro post as a draft for your review
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so mk-audience, mk-brand-kit, mk-community, mk-copy, mk-first-contact-audit, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:marketing-lead`, or let it start on its own when your request matches.

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

This installs the whole go-to-market pack, so mk-audience, mk-brand-kit, mk-community, mk-copy, mk-first-contact-audit, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:marketing-lead`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill marketing-lead
```

Skills arrive without a pack prefix: `/marketing-lead` in most agents and `@marketing-lead` in Windsurf. opencode shows `/marketing-lead` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/marketing-lead .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `marketing-lead` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r marketing-lead.zip marketing-lead
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `marketing-lead.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
