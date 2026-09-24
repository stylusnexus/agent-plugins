# Product Strategy

A chief product manager and teacher, thirteen focused skills and a business-capability specialist for deciding what to build and why. Built for product managers and for people with no product training: it starts from what you already know, labels evidence and assumptions, explains each choice, and leaves the decisions with you.

---

## The skills

| Skill | Use it when |
|---|---|
| `product-manager` | You want a chief PM to lead the work end to end, or to teach you while you do it. Routes to the skills below. |
| `pm-vision` | Defining a mission, vision, or winning aspiration: what success should mean. |
| `pm-strategy` | Choosing where to play and how to win, and the trade-offs that come with it. |
| `pm-strategy-fit` | Checking that strategic choices reinforce each other and are hard to copy. |
| `pm-canvas` | Filling in, teaching, or reviewing a one-page product strategy canvas. |
| `pm-value-proposition` | Working out customer value, alternatives, and a value curve. |
| `pm-objectives` | Setting OKRs, key metrics, or a North Star metric. Includes a 40-entry metric catalog. |
| `pm-roadmap` | Building an outcome roadmap, prioritizing, or writing a PRD or user stories. |
| `pm-discovery` | Planning interviews, testing assumptions, Kano surveys, journey maps, or A/B tests. |
| `pm-growth` | Acquisition, activation, retention, referral loops, and monetization. |
| `pm-market-analysis` | Five Forces, PESTLE, SWOT, and other views of the market around you. |
| `pm-capabilities` | Mapping the business capabilities a strategy needs, and the gaps. |
| `pm-teams` | Setting up empowered product teams and team-level objectives. |
| `pm-visuals` | Turning any of the above into a diagram (Mermaid by default) or an HTML page. |

Two Claude Code agents ship alongside: `product-manager` (the same chief PM, in its own context) and `business-capability-modeler`.

---

## Rule ownership

`product-manager` owns sequencing and teaching; each `pm-*` skill owns one artifact. When two could fire, the more specific skill wins: "draft our OKRs" goes to `pm-objectives`, "help me figure out what to do next with this product" goes to `product-manager`. `pm-visuals` never decides content; it draws what the other skills produced.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install product-strategy@stylus-nexus
```

Skills are namespaced: `/product-strategy:product-manager`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add product-strategy@stylus-nexus
```

In Codex, type `$product-manager` (or any skill name after `$`) to use a skill, or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill '*'
```

Skills arrive un-namespaced on this path, so they invoke as `/product-manager`.

## Prerequisites

None for the skills. The two bundled scripts need Python 3 and the standard library only: `scripts/metrics_lookup.py` searches the metric catalog, and `scripts/discovery_digest.py` summarizes a local file of research evidence. Neither makes network calls.

## Sources

Methods are credited to their originators, and every source is public. See the [source list](skills/product-manager/references/sources.md).
