<!-- skill-readme:begin -->
# mk-lifecycle

This skill should be used when the user asks for a waitlist sequence, onboarding emails, an activation email flow, a win-back or upgrade email, a lifecycle map, or how to nurture signups toward paying.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You have sign-ups and need emails that move them to active use.

**Try:** `Map the waitlist stages for Plant Ledger and draft a three-email onboarding sequence.`

**Skip it when:** You have no contacts yet. Find your audience first.

## What it looks like

Example output, invented data (fictional product). Emails fire on what someone did, not on a fixed day count.

| Stage | What moves someone in | Recorded in | Next-stage trigger |
|---|---|---|---|
| Waitlist | joined the waitlist | email tool | invite accepted |
| Signed up | account created | product database | adds a second room |
| Activated | 2+ rooms set up | product database | waters on schedule in week 2 |

| # | Trigger | Goal | The one ask |
|---|---|---|---|
| 1 | signed up | set expectations | add your first room |
| 2 | no second room after 3 days | remove the blocker | add one more room |
| 3 | second room added | point at the next win | turn on travel mode |

Results are read from clicks, replies, and unsubscribes. Open rate is context only.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-lifecycle`, or let it start on its own when your request matches.

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

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-lifecycle`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-lifecycle
```

Skills arrive without a pack prefix: `/mk-lifecycle` in most agents and `@mk-lifecycle` in Windsurf. opencode shows `/mk-lifecycle` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-lifecycle .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-lifecycle` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-lifecycle.zip mk-lifecycle
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-lifecycle.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
