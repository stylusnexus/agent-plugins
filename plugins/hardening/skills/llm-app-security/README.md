<!-- skill-readme:begin -->
# llm-app-security

Use when a product feature sends untrusted content to a language model or lets a model call tools, write data, send messages, or render output to other users. Triggers: a new chat, RAG, summarization, agent, or tool-calling feature; a model that reads web pages, documents, emails, tickets, or other users' text; a 'can prompt injection reach this' question; a pre-launch review of anything with an LLM in the request path; or an incident where a model did something nobody asked for.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Builds the input-to-sink table from a description; the AgentArmor scan, corpus run and staging test cannot run.

Part of the [hardening](../../README.md) pack.

## When and how to use it

**Use it when:** You ship a chat or document feature where a model reads untrusted text or calls tools.

**Try:** `Trace every path from user input to a model tool or output in the support chat feature.`

**Skip it when:** No model reads untrusted content or calls tools in the feature.

## What it looks like

*Example output, invented data.*

```text
| Input            | Sink               | Control                     | Location                     | Status |
| uploaded PDF     | email tool         | None                        | lib/agent/tools.ts:40 (here) | FAIL   |
| user message     | rendered Markdown  | link and image allowlist    | components/Answer.tsx:12     | PASS   |
| retrieved ticket | model prompt       | ingest scan, quoted as data | lib/rag/ingest.ts:88         | PASS   |

Corpus: public LLM test set at <commit> + 4 inert canary items
| Path          | Run   | Ingest | Output | Denied | Reached sink        |
| PDF -> email  | 4/4   | 0      | 0      | 0      | 1   <- blocks launch |
| msg -> render | 60/60 | 0      | 58     | 2      | 0                   |
False positives on 200 benign documents: 1 (0.5%)
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install hardening@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install hardening@stylus-nexus` do the same. This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it.

Call it as `/hardening:llm-app-security`, or let it start on its own when your request matches.

</details>

<details>
<summary>Claude Code desktop app</summary>

The desktop app's local sessions read the same plugin settings as the CLI, so a pack you installed from the terminal at user scope is already there.

To install from the app, add the marketplace once from a terminal with `claude plugin marketplace add stylusnexus/agent-plugins`. Then, in a local or SSH session on the **Code** tab, click **+** next to the prompt box, choose **Plugins**, then **Add plugin**, and pick **hardening**. Plugins do not load in the app's cloud sessions.

</details>

<details>
<summary>Codex</summary>

```bash
codex plugin marketplace add stylusnexus/agent-plugins
codex plugin add hardening@stylus-nexus
```

This installs the whole hardening pack, so agent-tooling-review, auth-hardening, exposure-scan, legal-docs, privacy-audit, rate-limit-audit, readiness-review, secrets-leak-audit, security-headers, threat-model and webhook-reliability come with it. In Codex, type `$` and the skill name (`$hardening:llm-app-security`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill llm-app-security
```

Skills arrive without a pack prefix: `/llm-app-security` in most agents and `@llm-app-security` in Windsurf. opencode shows `/llm-app-security` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/hardening/skills/llm-app-security .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `llm-app-security` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/hardening/skills
   zip -r llm-app-security.zip llm-app-security
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `llm-app-security.zip`.

**Limit:** Builds the input-to-sink table from a description; the AgentArmor scan, corpus run and staging test cannot run.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole hardening pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Builds the input-to-sink table from a description; the AgentArmor scan, corpus run and staging test cannot run.

</details>
<!-- skill-readme:end -->
