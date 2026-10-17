<!-- skill-readme:begin -->
# ux-review

Reviews Playwright visual-snapshot screenshots (or any screenshot folder) against a UX checklist — layout, spacing, hierarchy, consistency, accessibility, and mobile responsiveness — and reports a rating and findings per screenshot; files GitHub issues only when asked. Use on '/ux-review', 'review these screenshots', 'check the UI on mobile', or 'do a visual UX pass'.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: You upload screenshots by hand; no snapshot discovery, diff mode or Playwright refresh. Other agents: Reading screenshots as images is the whole job, and image reading is not verified for each host.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** You have screenshots of a screen and want layout, spacing and mobile problems listed.

**Try:** `/ux-review ./screenshots/settings-mobile.png`

**Skip it when:** The project has no screenshots and no visual tests to take them, or you want a code review.

## What it looks like

Example output, invented data.

```text
### settings-mobile.png
**Rating:** 🟡 Needs Attention

**Issues:**
- [Major] Save button sits below the fold on a 390px screen — move it into a sticky footer
- [Minor] Section headers and body text are the same weight — make headers bolder

**Positives:**
- Form fields stack cleanly with visible labels

UX Review Complete:
- Screenshots reviewed: 6
- 🟢 Good: 4   🟡 Needs Attention: 1   🔴 Needs Fix: 1
- Issues filed: 0 — not filed; reply 'file issues' to file them
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue and stripe-billing come with it.

Call it as `/ship-pipeline:ux-review`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **ship-pipeline**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add ship-pipeline@stylus-nexus
```

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue and stripe-billing come with it. In Codex, type `$` and the skill name (`$ship-pipeline:ux-review`), or run `/skills` to pick it.

**Note:** Needs the host to read screenshots as images, not verified for Codex.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill ux-review
```

Skills arrive without a pack prefix: `/ux-review` in most agents and `@ux-review` in Windsurf. opencode shows `/ux-review` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Reading screenshots as images is the whole job, and image reading is not verified for each host.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/ux-review .agents/skills/
```

**Limit:** Reading screenshots as images is the whole job, and image reading is not verified for each host.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `ux-review` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/ship-pipeline/skills
   zip -r ux-review.zip ux-review
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `ux-review.zip`.

**Limit:** You upload screenshots by hand; no snapshot discovery, diff mode or Playwright refresh.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole ship-pipeline pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** You upload screenshots by hand; no snapshot discovery, diff mode or Playwright refresh.

</details>
<!-- skill-readme:end -->
