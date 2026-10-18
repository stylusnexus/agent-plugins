<!-- skill-readme:begin -->
# mk-founder-content

This skill should be used when the user asks for founder posts, building in public, LinkedIn or social content, a blog post, a tweet or X/Bluesky post, a newsletter, personal brand content, a story for a launch, what should I post, or a weekly content plan for a founder.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You must post each week but have no idea what to write.

**Try:** `Turn my note on why I built Plant Ledger into a week of posts.`

**Skip it when:** You want to post in a forum or Discord, or write to one person. Use mk-community or mk-outreach.

## What it looks like

Example output, invented data (fictional product). One substantial piece, then short posts cut from it. Nothing is scheduled until the owner approves.

| Angle | Platform | One-line point | Real fact used | Status |
|---|---|---|---|---|
| The finding | LinkedIn | collectors lose plants after trips, not on normal weeks | 6 of 6 interviews (invented) | drafted |
| The how | Bluesky | build the schedule per room, not per plant | release notes v0.4 | drafted |
| The proof | LinkedIn | MISSING INFORMATION: needs a beta result from owner | none yet | blocked |
| The question | Bluesky | how do you handle watering when you travel? | n/a | not started |

Hours this week: 2. Stop rule: if waitlist sign-ups from posts don't move after 4 weeks, post less often and change the topic.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-first-contact-audit, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-founder-content`, or let it start on its own when your request matches.

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

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-first-contact-audit, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-founder-content`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-founder-content
```

Skills arrive without a pack prefix: `/mk-founder-content` in most agents and `@mk-founder-content` in Windsurf. opencode shows `/mk-founder-content` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-founder-content .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-founder-content` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-founder-content.zip mk-founder-content
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-founder-content.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
