<!-- skill-readme:begin -->
# mk-first-contact-audit

This skill should be used when the user asks why nobody is using their product, whether a landing page or README makes sense to a stranger, why visitors leave, whether people trust the site, why it is not found or shared well, or wants a diagnosis of a page before any copy is rewritten.

[![Claude: Code full, app full](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT full](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%94-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

Part of the [go-to-market](../../README.md) pack.

## When and how to use it

**Use it when:** People visit and do not sign up, and you do not know which part of the page is failing them.

**Try:** `Audit plantledger.example as a stranger would see it. The truth: a watering scheduler for people with 20+ houseplants who travel.`

**Skip it when:** You already know the cause and need the fix. Go straight to the skill that owns it.

## What it looks like

Example output, invented data (fictional product). Readers saw only their own stage's slice; the truth was kept from them.

```text
FIRST-CONTACT SCORECARD   plantledger.example   2026-03-02
Truth (kept from readers)  watering scheduler for people with 20+ houseplants who travel
Stage            Who        Problem    Differentiation   Confidence
1 headline       missing    partly     not stated        35
2 first screen   partly     matched    not stated        55
3 whole page     matched    matched    not stated        68
Time to confidence: never (needs 70 or more with who and problem matched)

Check                  Result   Evidence                                       Tag
2 Comprehension        Concern  "Smarter plant care" ... reader: "an app for plants"  multi-reader
4 Claim typing         Fail     9 of 10 headings are bare features              mechanical
6b Trust surfaced      Concern  export and delete appear only in a footer link   mechanical
8 Machine legibility   Fail     raw HTML holds 0 visible characters; title is the bare name   mechanical

Top fixes (earliest failing class first)
1 Headline names no problem and no person   -> mk-positioning, then mk-copy
2 Headings list features, not outcomes      -> mk-copy
3 Raw HTML is an empty shell                -> mk-search
Hypotheses to verify: "name reads oddly aloud" (LLM-only; ask 3 people to spell it back)
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install go-to-market@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install go-to-market@stylus-nexus` do the same. This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it.

Call it as `/go-to-market:mk-first-contact-audit`, or let it start on its own when your request matches.

**Note:** Uses the cold-reader agent that ships with the Claude Code plugin.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **go-to-market**. Plugins do not load in the app's cloud sessions.

**Note:** Uses the cold-reader agent that ships with the Claude Code plugin.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add go-to-market@stylus-nexus
```

This installs the whole go-to-market pack, so marketing-lead, mk-audience, mk-brand-kit, mk-community, mk-copy, mk-founder-content, mk-launch, mk-lifecycle, mk-measurement, mk-outreach, mk-positioning and mk-search come with it. In Codex, type `$` and the skill name (`$go-to-market:mk-first-contact-audit`), or run `/skills` to pick it.

**Note:** Without the cold-reader agent, each stage of the staged read runs by hand in its own fresh context. If the raw-HTML script cannot run or reach the page, the same signals are read by hand from the page source.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill mk-first-contact-audit
```

Skills arrive without a pack prefix: `/mk-first-contact-audit` in most agents and `@mk-first-contact-audit` in Windsurf. opencode shows `/mk-first-contact-audit` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Without the cold-reader agent, each stage of the staged read runs by hand in its own fresh context. If the raw-HTML script cannot run or reach the page, the same signals are read by hand from the page source.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/go-to-market/skills/mk-first-contact-audit .agents/skills/
```

**Note:** Without the cold-reader agent, each stage of the staged read runs by hand in its own fresh context. If the raw-HTML script cannot run or reach the page, the same signals are read by hand from the page source.

</details>

<details>
<summary>Claude app</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `mk-first-contact-audit` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/go-to-market/skills
   zip -r mk-first-contact-audit.zip mk-first-contact-audit
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `mk-first-contact-audit.zip`.

**Note:** Without the cold-reader agent, each stage of the staged read runs by hand in its own fresh context. If the raw-HTML script cannot run or reach the page, the same signals are read by hand from the page source.

</details>

<details>
<summary>ChatGPT</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole go-to-market pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Note:** Without the cold-reader agent, each stage of the staged read runs by hand in its own fresh context. If the raw-HTML script cannot run or reach the page, the same signals are read by hand from the page source.

</details>
<!-- skill-readme:end -->
