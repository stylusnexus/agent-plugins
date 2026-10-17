<!-- skill-readme:begin -->
# llm-council

Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final verdict. Based on Karpathy's LLM Council methodology. MANDATORY TRIGGERS: 'council this', 'run the council', 'war room this', 'pressure-test this', 'stress-test this', 'debate this'. STRONG TRIGGERS (use when combined with a real decision or tradeoff): 'should I X or Y', 'which option', 'what would you do', 'is this the right move', 'validate this', 'get multiple perspectives', 'I can't decide', 'I'm torn between'. Do NOT trigger on simple yes/no questions, factual lookups, or casual 'should I' without a meaningful tradeoff (e.g. 'should I use markdown' is not a council question). DO trigger when the user presents a genuine decision with stakes, multiple options, and context that suggests they want it pressure-tested from multiple angles.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: partial](https://img.shields.io/badge/Other%20agents-%E2%97%90-yellow)](../../../../README.md#compatibility)

> **Limits.** Claude app: No subagents, so the advisors are role-played in one context and lose the independence the method relies on. ChatGPT: No subagents documented, so the advisors are role-played in one context and lose their independence. Other agents: Uses subagents where the host documents them (Cursor, Gemini CLI/Antigravity CLI, opencode); on Copilot, Windsurf or Cline it falls back to a same-context council that loses the advisors' independence.

Part of the [second-opinion](../../README.md) pack.

## When and how to use it

**Use it when:** You must choose between options and a wrong call is costly.

**Try:** `Council this: free tier or 14-day trial for our analytics tool?`

**Skip it when:** The question has one right answer, or you only want a draft written.

## What it looks like

*Example output, invented data.*

```text
Question: free tier or 14-day trial for a small analytics tool?

Positions          Free tier   Trial   Reframe
Contrarian                      x
First Principles                         x   "who actually converts?"
Expansionist          x
Outsider                        x
Executor                        x

## Where the Council Agrees     the trial's deadline drives the decision to pay
## Where the Council Clashes    reach (free tier) against support load (trial)
## Blind Spots the Council Caught
   the Outsider could not tell from the pricing page what the tool does
## The Recommendation           ship the 14-day trial; revisit a free tier later
## The One Thing to Do First    rewrite the pricing page headline around the outcome

Files: council-report-<timestamp>.html, council-transcript-<timestamp>.md
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install second-opinion@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install second-opinion@stylus-nexus` do the same. This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, efficient-frontier-routing, plan-arbiter and spec-review come with it.

Call it as `/second-opinion:llm-council`, or let it start on its own when your request matches.

**Note:** Runs 11 subagents of the same model, so the advisors are independent passes, not different models.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **second-opinion**. Plugins do not load in the app's cloud sessions.

**Note:** Runs 11 subagents of the same model, so the advisors are independent passes, not different models.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

This installs the whole second-opinion pack, so agent-watchdog, debug-feedback-loop, efficient-frontier-routing, plan-arbiter and spec-review come with it. In Codex, type `$` and the skill name (`$second-opinion:llm-council`), or run `/skills` to pick it.

**Note:** Uses Codex subagents of the same model, so the advisors are independent passes, not different models.

</details>

<details>
<summary>Other agents, Skills CLI (partial)</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill llm-council
```

Skills arrive without a pack prefix: `/llm-council` in most agents and `@llm-council` in Windsurf. opencode shows `/llm-council` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Limit:** Uses subagents where the host documents them (Cursor, Gemini CLI/Antigravity CLI, opencode); on Copilot, Windsurf or Cline it falls back to a same-context council that loses the advisors' independence.

</details>

<details>
<summary>Other agents, by folder (partial)</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/second-opinion/skills/llm-council .agents/skills/
```

**Limit:** Uses subagents where the host documents them (Cursor, Gemini CLI/Antigravity CLI, opencode); on Copilot, Windsurf or Cline it falls back to a same-context council that loses the advisors' independence.

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `llm-council` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/second-opinion/skills
   zip -r llm-council.zip llm-council
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `llm-council.zip`.

**Limit:** No subagents, so the advisors are role-played in one context and lose the independence the method relies on.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole second-opinion pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** No subagents documented, so the advisors are role-played in one context and lose their independence.

</details>
<!-- skill-readme:end -->
