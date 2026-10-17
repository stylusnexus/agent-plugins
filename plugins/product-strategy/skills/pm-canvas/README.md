<!-- skill-readme:begin -->
# pm-canvas

Use when the user asks to build, fill in, teach, review, or update a one-page product strategy canvas covering winning aspiration, where to play, how to win, capabilities, and management systems.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Each upload is one skill folder, so the shared-principles file this skill reads from a sibling skill is missing unless you bundle it in.

Part of the [product-strategy](../../README.md) pack.

## When and how to use it

**Use it when:** You want the whole strategy on one page for a team review.

**Try:** `Fill in a strategy canvas for my plant watering tracker.`

**Skip it when:** You need depth on one choice, such as a full value curve.

## What it looks like

Example output, invented data (fictional product). Every entry carries a status: evidence-backed, hypothesis, or accepted.

```text
PRODUCT STRATEGY CANVAS: Plant Ledger         Status: Draft
1 Winning aspiration  First tracker collectors recommend          [hypothesis]
2 Where to play       Collectors with 20+ indoor plants           [evidence-backed]
                      Not: casual owners, plant shops (for now)   [accepted]
3 How to win          Room-by-room schedules that survive travel  [hypothesis]
                      Who could copy it? Any app. Why won't they? Setup cost for casual users
4 Capabilities        Schedule engine (have it); care data (do not have it)
5 Management systems  Weekly missed-watering review, one owner    [accepted]
Key measures          Collectors still active at week 4: baseline unknown
Open assumptions      The app actually has every capability claimed in section 4: check against what has shipped
Main strategic fork   Collectors over everyone: gives up the mass market
```

## Install

This skill reads shared files in its sibling skills, so install the whole product-strategy pack. The Claude Code and Codex plugins do that already; with the Skills CLI or a folder copy, take every skill in the pack.

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install product-strategy@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install product-strategy@stylus-nexus` do the same. This installs the whole product-strategy pack, so pm-capabilities, pm-discovery, pm-growth, pm-market-analysis, pm-objectives, pm-roadmap, pm-strategy, pm-strategy-fit, pm-teams, pm-value-proposition, pm-vision, pm-visuals, pricing-review and product-manager come with it.

Call it as `/product-strategy:pm-canvas`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **product-strategy**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add product-strategy@stylus-nexus
```

This installs the whole product-strategy pack, so pm-capabilities, pm-discovery, pm-growth, pm-market-analysis, pm-objectives, pm-roadmap, pm-strategy, pm-strategy-fit, pm-teams, pm-value-proposition, pm-vision, pm-visuals, pricing-review and product-manager come with it. In Codex, type `$` and the skill name (`$product-strategy:pm-canvas`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

This skill reads shared files in its sibling skills, so install every skill in the pack:

```bash
npx skills add stylusnexus/agent-plugins --skill pm-canvas pm-capabilities pm-discovery pm-growth pm-market-analysis pm-objectives pm-roadmap pm-strategy pm-strategy-fit pm-teams pm-value-proposition pm-vision pm-visuals pricing-review product-manager
```

Skills arrive without a pack prefix: `/pm-canvas` in most agents and `@pm-canvas` in Windsurf. opencode shows `/pm-canvas` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Install the whole pack: this skill reads shared files in a sibling skill.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy every skill in the pack, so the shared files sit beside this one:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/product-strategy/skills/. .agents/skills/
```

**Note:** Install the whole pack: this skill reads shared files in a sibling skill.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `pm-canvas` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/product-strategy/skills
   zip -r pm-canvas.zip pm-canvas
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `pm-canvas.zip`.

**Limit:** Each upload is one skill folder, so the shared-principles file this skill reads from a sibling skill is missing unless you bundle it in.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole product-strategy pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
