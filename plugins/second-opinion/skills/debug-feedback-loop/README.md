<!-- skill-readme:begin -->
# debug-feedback-loop

Construct a fast, deterministic pass/fail signal for a bug BEFORE hypothesising — the missing mechanics behind "reproduce the bug". Offers a ladder of loop-construction techniques (failing test, curl/CLI harness, headless browser, trace replay, bisection, fuzz, differential), ranked falsifiable hypotheses, and tagged-instrumentation cleanup. Use when a bug is hard to reproduce, flaky/non-deterministic, lacks an obvious repro, or when getting a reliable signal is the bottleneck. Complements (does not replace) systematic-debugging, which owns root-cause discipline — reach for this when the hard part is getting a signal, not staying disciplined. Use only when the user explicitly asks for it ("/debug-feedback-loop", "build a feedback loop for this bug"); do not start it on your own.

[![Claude: Code full, app no](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT no](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%9C%96-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app: The loop needs a shell. ChatGPT: No access to your local repo or git and gh credentials by default.

Part of the [second-opinion](../../README.md) pack.

## When and how to use it

**Use it when:** A bug is flaky or hard to repeat and you need a reliable pass or fail check first.

**Try:** `/debug-feedback-loop the cart total is wrong about one time in ten`

**Skip it when:** The bug already has a reliable failing test. Move on to finding the root cause.

## What it looks like

*Example exchange, invented data. This skill runs only when you invoke it.*

```text
You:   /debug-feedback-loop  Checkout total is sometimes off by one cent.

Agent: Loop: property loop (ladder step 7), 1000 random carts against the
       totals function, seeded. Reproduces 31 of 1000 in 2 seconds.

       Hypotheses, ranked, before testing any:
       1. If float rounding is the cause, integer cents makes all 31 disappear.
       2. If discount order is the cause, applying tax first changes the count.
       3. If currency conversion is the cause, a USD-only run drops to 0.

       Probes tagged [DBG-a4f2]; one grep removes them after the fix.
       Regression test goes in before the fix, at the totals seam.
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install second-opinion@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install second-opinion@stylus-nexus` do the same. This installs the whole second-opinion pack, so agent-watchdog, efficient-frontier-routing, llm-council, plan-arbiter and spec-review come with it.

Call it as `/second-opinion:debug-feedback-loop`, or let it start on its own when your request matches.

**Note:** Only the description's "use only when asked" wording keeps it from triggering on its own; there is no hard switch.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **second-opinion**. Plugins do not load in the app's cloud sessions.

**Note:** Only the description's "use only when asked" wording keeps it from triggering on its own; there is no hard switch.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add second-opinion@stylus-nexus
```

This installs the whole second-opinion pack, so agent-watchdog, efficient-frontier-routing, llm-council, plan-arbiter and spec-review come with it. In Codex, type `$` and the skill name (`$second-opinion:debug-feedback-loop`), or run `/skills` to pick it.

**Note:** Only the description's "use only when asked" wording keeps it from triggering on its own; there is no hard switch.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill debug-feedback-loop
```

Skills arrive without a pack prefix: `/debug-feedback-loop` in most agents and `@debug-feedback-loop` in Windsurf. opencode shows `/debug-feedback-loop` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

**Note:** Only the description's "use only when asked" wording keeps it from triggering on its own; there is no hard switch.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/second-opinion/skills/debug-feedback-loop .agents/skills/
```

**Note:** Only the description's "use only when asked" wording keeps it from triggering on its own; there is no hard switch.

</details>

<details>
<summary>Claude app: not supported</summary>

**Why:** The loop needs a shell.

</details>

<details>
<summary>ChatGPT: not supported</summary>

**Why:** No access to your local repo or git and gh credentials by default.

</details>
<!-- skill-readme:end -->
