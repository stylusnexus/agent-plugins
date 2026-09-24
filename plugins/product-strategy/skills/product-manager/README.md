# Product management suite

One chief PM, thirteen focused support skills, and a business-capability modeling specialist. Useful for commercial products, internal tools, open source, creative work, and personal projects. Guided co-working is the default — no PM background required. The chief walks through steps, explains concepts, drafts alongside you, and helps you decide. Ask for a slower workshop, a faster expert pass, or direct drafting whenever you'd rather have that instead.

## Install

### Claude Code
```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install product-strategy@stylus-nexus
```
Skills are namespaced: `/product-strategy:pm-strategy`, and so on. The chief PM skill is `/product-strategy:product-manager`.

### Codex
```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add product-strategy@stylus-nexus
```
In Codex, type `$product-manager` to use the skill, or run `/skills` to pick one ([Codex docs](https://developers.openai.com/codex/skills)).

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, and more
```bash
npx skills add stylusnexus/agent-plugins --skill '*'
```
Skills arrive un-namespaced on this path and invoke as `/product-manager`, `/pm-strategy`, etc.

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
