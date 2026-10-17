<!-- skill-readme:begin -->
# mk-community

This skill should be used when the user asks about Discord servers, subreddits, forums, open-source community building, GitHub issues and discussions as marketing, or participating in a hobby, enthusiast, or developer community.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** You want to take part in a forum, Discord, or subreddit.

**Try:** `Check the rules of r/houseplants, then draft a first post for Plant Ledger.`

**Skip it when:** You want to post in bulk. This skill drafts one post at a time for your review.

## What it looks like

Example output, invented data (fictional community). The rules page is fetched and dated before any post is drafted.

| Date | Community | Give | Ask | Response | Give:ask |
|---|---|---|---|---|---|
| 2026-09-02 | r/ExampleHouseplants (fictional) | rules fetched; answered 3 watering questions | none | 2 thanks, 1 follow-up | 3:0 |
| 2026-09-09 | r/ExampleHouseplants | shared a free watering-log template | none | 40 upvotes, 6 saves | 4:0 |
| 2026-09-16 | r/ExampleHouseplants | answered 2 questions | posted a build update in the weekly self-promo thread, per rule 4 | 5 comments, no complaints | 6:1 |

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-community`, or let it start on its own when your request matches.

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

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-community`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-community
```

Skills arrive without a pack prefix: `/mk-community` in most agents and `@mk-community` in Windsurf. opencode shows `/mk-community` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-community .agents/skills/
```

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-community` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-community.zip mk-community
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-community.zip`.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
