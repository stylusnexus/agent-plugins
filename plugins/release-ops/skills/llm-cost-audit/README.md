<!-- skill-readme:begin -->
# llm-cost-audit

Measure and reduce what a product pays for LLM calls - reconcile tracked cost with the provider's bill, check each call site's model tier, find prompt-caching and batch candidates, check that bring-your-own-key paths stay user-paid, and set budget alerts. Ends in a savings table with the cost-per-call arithmetic shown. Use for "audit our AI spend", "why is our model API bill high", "reduce LLM costs", or as a periodic cost-hygiene pass.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Works on uploaded bills, usage exports and pasted call sites; no search across the repo.

Part of the [release-ops](../../README.md) pack.

## When and how to use it

**Use it when:** Your model API bill is high and you want to know where the money goes.

**Try:** `Audit our AI spend and show the savings with the arithmetic.`

**Skip it when:** You only want to pick a model for one new task.

## What it looks like

Example output, invented data. Prices are illustrative, not current; the skill reads them from each provider's pricing page on the day of the audit.

```text
Spend: tracked $2,430/mo, billed $2,610/mo. Gap of $180: the retry path in
  jobs/retry.ts:22 skips the tracking wrapper (fix: wrap it).

classify-ticket, top tier → small tier (50 sampled outputs, no regression)
  now:   (1,200 × $5 + 20 × $25) / 1M = $0.0065 × 300,000 calls = $1,950/mo
  after: (1,200 × $1 + 20 × $5)  / 1M = $0.0013 × 300,000 calls =   $390/mo
nightly-tagging, mid tier, synchronous → batch API at 50%
  now:   (3,000 × $2 + 200 × $10) / 1M = $0.008 × 60,000 calls = $480/mo → $240/mo

Finding                  Current   Action                Savings   Price source
classify on top tier     $1,950    route to small tier   $1,560    pricing URL, date read
nightly tagging is sync    $480    move to batch API       $240    pricing URL, date read
Total                    $2,430                          $1,800
Safe to ship now: routing. Needs a test pass first: batch.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install release-ops@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install release-ops@stylus-nexus` do the same. This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, npm-publish, observability-setup, pr-wait, the-waiting, version-check and vscode-marketplace-publish come with it.

Call it as `/release-ops:llm-cost-audit`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **release-ops**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add release-ops@stylus-nexus
```

This installs the whole release-ops pack, so customer-support-triage, dependency-upgrade, incident-response, npm-publish, observability-setup, pr-wait, the-waiting, version-check and vscode-marketplace-publish come with it. In Codex, type `$` and the skill name (`$release-ops:llm-cost-audit`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill llm-cost-audit
```

Skills arrive without a pack prefix: `/llm-cost-audit` in most agents and `@llm-cost-audit` in Windsurf. opencode shows `/llm-cost-audit` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/release-ops/skills/llm-cost-audit .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `llm-cost-audit` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/release-ops/skills
   zip -r llm-cost-audit.zip llm-cost-audit
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `llm-cost-audit.zip`.

**Limit:** Works on uploaded bills, usage exports and pasted call sites; no search across the repo.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole release-ops pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Works on uploaded bills, usage exports and pasted call sites; no search across the repo.

</details>
<!-- skill-readme:end -->
