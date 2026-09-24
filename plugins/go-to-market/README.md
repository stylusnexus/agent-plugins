# Go-to-Market

A head of marketing and eleven focused skills for small teams and solo builders. Plans start from a goal and the hours you actually have, favour honest persuasion over tricks, keep evidence and assumptions separate, and explain the marketing reasoning as they go.

---

## The skills

| Skill | Use it when |
|---|---|
| `marketing-lead` | You want a marketing plan, or don't know why nobody is using the product. Routes to the skills below and teaches as it goes. |
| `mk-positioning` | Working out who the product is for, what it beats, and how to say it in one line. Built on April Dunford's positioning method. |
| `mk-audience` | Choosing the first customer, writing an ideal customer profile, and finding who influences the buyer. |
| `mk-copy` | Writing or editing a landing page, README opening, store listing, or announcement. |
| `mk-brand-kit` | Settling a product's voice, palette, fonts, and logo use, and picking a design tool. |
| `mk-search` | Getting found in search and cited by AI assistants: citable pages, `llms.txt`, test-question panels. |
| `mk-launch` | Planning a launch or relaunch: Show HN, Product Hunt, release-day posts, and the readout afterwards. |
| `mk-community` | Taking part in Discord servers, subreddits, forums, and open-source communities without spamming them. |
| `mk-founder-content` | Founder posts, building in public, newsletters, and finding the stories worth telling. |
| `mk-outreach` | Cold email, press and podcast pitches, design partners, and warm introductions. |
| `mk-lifecycle` | Waitlist, onboarding, activation, upgrade, and win-back email sequences. |
| `mk-measurement` | Choosing what to measure, reading whether a channel worked, and running trustworthy experiments. |

Two Claude Code agents ship alongside: `marketing-lead` (the same head of marketing, in its own context) and `audience-scout`, which finds the real online places an audience gathers and verifies each by fetching the page. It only reads; it never posts, joins, or messages.

---

## Rule ownership

`marketing-lead` owns the plan and the order of work; each `mk-*` skill owns one kind of output. Positioning comes before copy: `mk-copy` asks for a settled position from `mk-positioning` rather than inventing one. Product strategy is out of scope; when there is no clear customer or promise yet, the skills point to the [`product-strategy`](../product-strategy) plugin (`product-manager`, `pm-value-proposition`).

No skill posts, sends, or publishes anything on your behalf. Plans and drafts come back to you.

---

## Install

### Claude Code

```
/plugin marketplace add stylusnexus/agent-plugins
/plugin install go-to-market@stylus-nexus
```

Skills are namespaced: `/go-to-market:marketing-lead`.

### Codex

```
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add go-to-market@stylus-nexus
```

In Codex, type `$marketing-lead` (or any skill name after `$`) to use a skill, or run `/skills` to pick one.

### Everything else — Cursor, Copilot, Gemini CLI, Windsurf, Zed, opencode, Cline, Continue, Hermes, and ~60 more

```bash
npx skills add stylusnexus/agent-plugins --skill marketing-lead mk-audience mk-brand-kit mk-community mk-copy mk-founder-content mk-launch mk-lifecycle mk-measurement mk-outreach mk-positioning mk-search
```

Skills arrive un-namespaced on this path, so they invoke as `/marketing-lead`.

## Prerequisites

None. `audience-scout` uses web search and fetch where the host provides them.

## Sources

Methods are credited to their originators where one exists; books appear only as further reading. See the [source list](skills/marketing-lead/references/sources.md).
