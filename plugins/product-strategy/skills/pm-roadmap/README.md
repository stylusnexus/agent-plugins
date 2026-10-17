<!-- skill-readme:begin -->
# pm-roadmap

This skill should be used when the user asks for a roadmap, prioritization, now-next-later plan, product sequencing, or a feature backlog linked to outcomes.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [product-strategy](../../README.md) pack.

## When and how to use it

**Use it when:** You have many requests and need to order them by outcome.

**Try:** `Build a Now, Next, Later roadmap from my backlog of 12 feature requests.`

**Skip it when:** You have no objectives yet and cannot say what outcome you want.

## What it looks like

Example output, invented data (fictional product). Uses the `pm-visuals` outcome-roadmap layout. Later items stay tentative.

| Now | Next | Later |
|---|---|---|
| O1 More collectors set up 2+ rooms; test a guided room setup; exit when 60% of new users reach 2 rooms | O2 Fewer missed waterings while traveling; depends on O1 finding | O3 Plant shops as a second segment (option); revisit if 5 shops ask |
| Discovery: 5 interviews on why people skip room setup | Delivery: travel mode, first slice | Measurement: shop interest log |

Dates: none are commitments. Week 6 review is an estimate.

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install product-strategy@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install product-strategy@stylus-nexus` do the same. This installs the whole product-strategy pack, so pm-canvas, pm-capabilities, pm-discovery, pm-growth, pm-market-analysis, pm-objectives, pm-strategy, pm-strategy-fit, pm-teams, pm-value-proposition, pm-vision, pm-visuals, pricing-review and product-manager come with it.

Call it as `/product-strategy:pm-roadmap`, or let it start on its own when your request matches.

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

This installs the whole product-strategy pack, so pm-canvas, pm-capabilities, pm-discovery, pm-growth, pm-market-analysis, pm-objectives, pm-strategy, pm-strategy-fit, pm-teams, pm-value-proposition, pm-vision, pm-visuals, pricing-review and product-manager come with it. In Codex, type `$` and the skill name (`$product-strategy:pm-roadmap`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill pm-roadmap
```

Skills arrive without a pack prefix: `/pm-roadmap` in most agents and `@pm-roadmap` in Windsurf. opencode shows `/pm-roadmap` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/product-strategy/skills/pm-roadmap .agents/skills/
```

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `pm-roadmap` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/product-strategy/skills
   zip -r pm-roadmap.zip pm-roadmap
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `pm-roadmap.zip`.

**Note:** Optional cross-references to other pack skills need the whole pack.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole product-strategy pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->
