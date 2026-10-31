<!-- skill-readme:begin -->
# art-direction

Art direction for websites and app screens, forked from Leonxlnx's taste-skill v2 (MIT) with three optional house styles (soft, minimalist, brutalist) and variance/motion/density dials. Distilled from a study of 247 curated gallery sites (One Page Love, Awwwards Sites of the Day). Deals researched directions (idea, composition, type, palette, photographs, section blueprints) from a library, enforces a strict no-slop house style with a real-browser inspector, and runs a look-and-fix loop on screenshots. Use this whenever you build, design, redesign, restyle, polish or review a landing page, marketing site, portfolio, product page, one-pager, hero or any public-facing web page, in any stack (HTML/CSS, React, Next.js, Vue, Svelte, Astro, Tailwind) — also when the user says a page looks generic, templated, "AI-made", sloppy, or asks to make it look designed, premium, award-level or less like every other site. Also for app screens: dashboards, admin and analytics views, settings, inboxes and other screens people work in, with their own run and rules.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: No local Node or Chrome to run the direction, inspect, redesign-check and lint scripts; the written art-direction guidance still applies to pages you describe or paste. Other agents: The scripts (the inspector and the redesign check) need Node 22+ and a local Chrome-family browser (Chrome, Edge or Chromium); without them only the written guidance applies.

Part of the [design-suite](../../README.md) pack.

## When and how to use it

**Use it when:** A landing page, portfolio, product page or app screen looks generic or "AI-made" and you want a deliberate, researched look.

**Try:** `Art-direct the Quill landing page. Deal me directions and build the one I pick.`

**Skip it when:** You need an accessibility verdict, a flow or information architecture. Use the matching skill. Use `interface-polish` for small spacing and state fixes on a look that is already decided.

## What it looks like

Example output, invented data (fictional product). The directions and findings below are made up for the sample.

```text
Brief: Quill, invoicing for freelancers      Idea: "paid on time, quietly"
Dealt   1 Ledger paper (warm, serif)   2 Field notes (grid, mono accents)   3 Plain speech (large type, one colour)
Chosen  1 Ledger paper    Type: serif display + grotesque body    Palette: cream, ink, one green
Built   hero, how it works, pricing, FAQ     Section blueprints applied: 4
Inspect (real browser, 390 and 1440 px)
  hero headline overflows at 390 px             fixed: clamp() on the display size
  three equal icon cards under the hero         fixed: replaced by one worked example
  placeholder photo copy ("Lorem")              open: needs a real photograph
Lint: 0 slop patterns remaining
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install design-suite@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install design-suite@stylus-nexus` do the same. This installs the whole design-suite pack, so accessibility-review, dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it.

Call it as `/design-suite:art-direction`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **design-suite**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add design-suite@stylus-nexus
```

This installs the whole design-suite pack, so accessibility-review, dashboard-design, information-architecture, interface-polish, mobile-design and ui-ux come with it. In Codex, type `$` and the skill name (`$design-suite:art-direction`), or run `/skills` to pick it.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill art-direction
```

Skills arrive without a pack prefix: `/art-direction` in most agents and `@art-direction` in Windsurf. opencode shows `/art-direction` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** The scripts (the inspector and the redesign check) need Node 22+ and a local Chrome-family browser (Chrome, Edge or Chromium); without them only the written guidance applies.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/design-suite/skills/art-direction .agents/skills/
```

**Limit:** The scripts (the inspector and the redesign check) need Node 22+ and a local Chrome-family browser (Chrome, Edge or Chromium); without them only the written guidance applies.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `art-direction` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/design-suite/skills
   zip -r art-direction.zip art-direction
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `art-direction.zip`.

**Limit:** No local Node or Chrome to run the direction, inspect, redesign-check and lint scripts; the written art-direction guidance still applies to pages you describe or paste.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole design-suite pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** No local Node or Chrome to run the direction, inspect, redesign-check and lint scripts; the written art-direction guidance still applies to pages you describe or paste.

</details>
<!-- skill-readme:end -->
