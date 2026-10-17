<!-- skill-readme:begin -->
# product-manager

This skill should be used when the user asks for a chief PM, product management help, product direction, strategy, or teaching while developing mission, vision, winning aspiration, value proposition, objectives, metrics, roadmaps, and growth.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: Each upload is one skill folder, so the sibling skills this one routes to are missing unless you upload them too.

Part of the [product-strategy](../../README.md) pack.

## When and how to use it

**Use it when:** You have a product idea and do not know what to work on first.

**Try:** `I built a watering tracker for houseplant collectors. Where do I start?`

**Skip it when:** You already know which single artifact you need, such as OKRs or a roadmap.

## What it looks like

Example exchange, invented data (fictional product).

```text
You:    I built a watering tracker for houseplant collectors. What should I do next?

Agent:  Route: why it exists > where to compete > customer value > measures > roadmap
        Current step: why it exists, and for whom
        Draft:    help collectors with 20+ plants stop losing plants to a missed watering
        Option A: hobby collectors   (evidence: all 40 beta users collect plants)
        Option B: small plant shops  (hypothesis: no shop has used it yet)
        Recommend A, because the evidence supports it. B stays open as a later test.
        Unknown:  whether people keep using it after week 2 (no data yet)
        One question for you: is this a paid product, or a personal tool for now?
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

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install product-strategy@stylus-nexus` do the same. This installs the whole product-strategy pack, so pm-canvas, pm-capabilities, pm-discovery, pm-growth, pm-market-analysis, pm-objectives, pm-roadmap, pm-strategy, pm-strategy-fit, pm-teams, pm-value-proposition, pm-vision, pm-visuals and pricing-review come with it.

Call it as `/product-strategy:product-manager`, or let it start on its own when your request matches.

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

This installs the whole product-strategy pack, so pm-canvas, pm-capabilities, pm-discovery, pm-growth, pm-market-analysis, pm-objectives, pm-roadmap, pm-strategy, pm-strategy-fit, pm-teams, pm-value-proposition, pm-vision, pm-visuals and pricing-review come with it. In Codex, type `$` and the skill name (`$product-strategy:product-manager`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

This skill reads shared files in its sibling skills, so install every skill in the pack:

```bash
npx skills add stylusnexus/agent-plugins --skill pm-canvas pm-capabilities pm-discovery pm-growth pm-market-analysis pm-objectives pm-roadmap pm-strategy pm-strategy-fit pm-teams pm-value-proposition pm-vision pm-visuals pricing-review product-manager
```

Skills arrive without a pack prefix: `/product-manager` in most agents and `@product-manager` in Windsurf. opencode shows `/product-manager` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Install the whole pack: this skill routes to its sibling skills.

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

**Note:** Install the whole pack: this skill routes to its sibling skills.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `product-manager` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/product-strategy/skills
   zip -r product-manager.zip product-manager
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `product-manager.zip`.

**Limit:** Each upload is one skill folder, so the sibling skills this one routes to are missing unless you upload them too.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole product-strategy pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

</details>
<!-- skill-readme:end -->

## Product management suite

One chief PM, thirteen focused support skills, and a business-capability modeling specialist. Useful for commercial products, internal tools, open source, creative work, and personal projects. Guided co-working is the default — no PM background required. The chief walks through steps, explains concepts, drafts alongside you, and helps you decide. Ask for a slower workshop, a faster expert pass, or direct drafting whenever you'd rather have that instead.

## Start here
Ask for the chief PM directly:

> Help me understand this project, then develop its direction and strategy. Explain the important decisions as we go.

Or ask to use the **product-manager agent** for bounded, non-interactive PM analysis (useful when you want a subagent to do research or draft options rather than hold the conversation). Keep interactive teaching and decisions in the main conversation; use the agent for self-contained work.

## Support skills
Invoke a skill directly when you know exactly what you need; otherwise let the chief route you there.

| Skill | Use it for |
|---|---|
| [pm-teams](../pm-teams/SKILL.md) | Empowered teams, strategic context, operating principles, Team Topologies |
| [pm-visuals](../pm-visuals/SKILL.md) | Editable diagrams and analysis, plus an offline example gallery |
| [pm-market-analysis](../pm-market-analysis/SKILL.md) | Five Forces, PESTLE/PESTEL, SWOT |
| [pm-vision](../pm-vision/SKILL.md) | Mission, vision, purpose, winning aspiration |
| [pm-strategy](../pm-strategy/SKILL.md) | Strategic choices, cost/differentiation focus, trade-offs |
| [pm-value-proposition](../pm-value-proposition/SKILL.md) | Customer value, alternatives, value curves, eliminate/reduce/raise/create |
| [pm-objectives](../pm-objectives/SKILL.md) | Objectives, OKRs, key metrics, baselines, guardrails |
| [pm-roadmap](../pm-roadmap/SKILL.md) | Outcome-based priorities, horizons, dependencies, initiative briefs |
| [pm-discovery](../pm-discovery/SKILL.md) | Research, assumption tests, experiments, pre-mortems |
| [pm-growth](../pm-growth/SKILL.md) | Growth, retention, marketing channels, distribution, monetization |
| [pm-capabilities](../pm-capabilities/SKILL.md) | Business capability maps, current/target gaps, build/buy/partner choices |
| [pm-strategy-fit](../pm-strategy-fit/SKILL.md) | Reinforcing choices, contradictions, can't/won't-copy tests |
| [pm-canvas](../pm-canvas/SKILL.md) | Full product strategy canvas synthesis and workshops |

The **business-capability-modeler** agent does focused capability analysis on request. A capability is what the business must be able to do — it isn't a feature, a team, or a piece of technology.

## Example requests
- "Develop a winning aspiration and compare where we could play. Explain the trade-offs."
- "Build a strategy canvas from our actual evidence. Label what we don't know."
- "Compare cost focus and differentiation focus for this product."
- "Build a value curve without inventing competitor ratings."
- "Map the capabilities this strategy needs and where we're currently weak."
- "Do these choices reinforce each other? What could a competitor copy?"
- "Turn this strategy into objectives, key metrics, and a Now/Next/Later roadmap."
- "Which channels fit this segment and value proposition? Propose small tests."
- "Workshop this with me, one decision at a time."

## Diagrams and analysis
Ask for a strategy canvas, value curve, capability map, fit/activity diagram, discovery double diamond, roadmap, Five Forces, PESTEL, or SWOT view. The suite pairs the visual with evidence, assumptions, and implications rather than handing back a picture alone. See [pm-visuals](../pm-visuals/SKILL.md).

## How it works
Understand → explore choices → explain implications → decide with the owner → test assumptions → measure and revise. Start at whichever decision is actually live, not necessarily step one. See [working with strategy](references/working-with-strategy.md).

A workshop can produce an initial, actionable strategy — discussion alone doesn't validate it. A strategy can be accepted and ready to act on while staying open to revision. Bring in real customer evidence and relevant product/design/engineering/business perspectives; talking to an AI about your users is not customer research.

## Sources and verification
See [sources](references/sources.md) for the public methods and primary sources this suite draws on, the [product strategy canvas template](../pm-canvas/templates/product-strategy-canvas.md) and [value proposition template](../pm-value-proposition/templates/value-proposition.md) for this plugin's own original layouts built on those public frameworks, and [verification](verification.md) for what's actually been checked. Frameworks inform judgment; they don't prove a product will succeed.

## License
MIT for the suite's own text and code, including both templates above. See the repository LICENSE.
