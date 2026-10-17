<!-- skill-readme:begin -->
# stripe-billing

Implement or review Stripe subscription billing in a Next.js App Router app — Checkout Sessions, customer portal, signed and idempotent webhook handler, plan changes and proration, trials, and dunning. Use when asked to "add subscriptions", "add a paywall", "review our billing code", or when a user "paid but is still on free", or a webhook, proration, or trial bug is reported.

[![Claude: Code full, app partial](https://img.shields.io/badge/Claude-Code%20%E2%9C%94%20%C2%B7%20app%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Codex / ChatGPT: Codex full, ChatGPT partial](https://img.shields.io/badge/Codex%20%2F%20ChatGPT-Codex%20%E2%9C%94%20%C2%B7%20ChatGPT%20%E2%97%90-brightgreen)](../../../../README.md#compatibility) [![Other agents: full](https://img.shields.io/badge/Other%20agents-%E2%9C%94-brightgreen)](../../../../README.md#compatibility)

> **Limits.** Claude app and ChatGPT: Writes billing code from pasted code; the Stripe CLI webhook test and database proof cannot run.

Part of the [ship-pipeline](../../README.md) pack.

## When and how to use it

**Use it when:** A user paid but is still on the free plan, or you are adding subscriptions.

**Try:** `A customer paid but is still on free. Review our Stripe webhook handler`

**Skip it when:** You only take one-off payments with no subscriptions.

## What it looks like

Example output, invented data.

```text
Handled: checkout.session.completed, customer.subscription.created,
  customer.subscription.updated, customer.subscription.deleted,
  invoice.paid, invoice.payment_failed, customer.subscription.trial_will_end
Not handled, on purpose: invoice.upcoming
Idempotency: event.id inserted into WebhookEvent (unique) in the same
  transaction as the state change

$ stripe trigger customer.subscription.updated
  before: status=trialing  priceId=price_basic
  after:  status=active    priceId=price_pro
$ stripe events resend evt_test_0412
  WebhookEvent rows before: 1   after: 1   (nothing written twice)
Handler forced to throw → 500; resend → 200, row written once
Client-supplied Stripe IDs trusted anywhere: none found
```

## Install

<details>
<summary>Claude Code (CLI)</summary>

Add the marketplace once, then install the pack:

```bash
claude plugin marketplace add stylusnexus/agent-plugins
claude plugin install ship-pipeline@stylus-nexus
```

Inside a session, `/plugin marketplace add stylusnexus/agent-plugins` and `/plugin install ship-pipeline@stylus-nexus` do the same. This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue and ux-review come with it.

Call it as `/ship-pipeline:stripe-billing`, or let it start on its own when your request matches.

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

This installs the whole ship-pipeline pack, so analytics-instrumentation, api-design, backup-verify, cdf, db-migration-safety, db-truth, deploy, feature-flags, prove-it, review-merge-pipeline, review-slop, ship-issues, start-issue and ux-review come with it. In Codex, type `$` and the skill name (`$ship-pipeline:stripe-billing`), or run `/skills` to pick it.

**Note:** Network steps need an approval or a network-enabled Codex profile.

</details>

<details>
<summary>Other agents, Skills CLI</summary>

The [Skills CLI](https://github.com/vercel-labs/skills) finds the agents you have and writes the skill into each one's skills folder.

```bash
npx skills add stylusnexus/agent-plugins --skill stripe-billing
```

Skills arrive without a pack prefix: `/stripe-billing` in most agents and `@stripe-billing` in Windsurf. opencode shows `/stripe-billing` only when the skill sets an opencode-specific metadata field, and Gemini CLI starts a skill itself after you approve it.

</details>

<details>
<summary>Other agents, by folder</summary>

`.agents/skills` is read by Codex, Gemini CLI, Antigravity CLI, Cursor, GitHub Copilot, opencode and Windsurf. Claude Code reads `.claude/skills`. Cline does not read `.agents/skills`; use `.cline/skills` or `.claude/skills` there.

Copy the skill folder:

```bash
git clone --depth 1 https://github.com/stylusnexus/agent-plugins
mkdir -p .agents/skills
cp -R agent-plugins/plugins/ship-pipeline/skills/stripe-billing .agents/skills/
```

</details>

<details>
<summary>Claude app (partial)</summary>

1. Turn on **Code execution and file creation** in **Settings > Capabilities**. On Team and Enterprise plans, an owner controls this.
2. Zip the skill folder, so the ZIP holds the `stripe-billing` folder:

   ```bash
   git clone --depth 1 https://github.com/stylusnexus/agent-plugins
   cd agent-plugins/plugins/ship-pipeline/skills
   zip -r stripe-billing.zip stripe-billing
   ```

3. In Claude, open **Customize > Skills**, click **+**, then **+ Create skill**, choose **Upload a skill** and pick `stripe-billing.zip`.

**Limit:** Writes billing code from pasted code; the Stripe CLI webhook test and database proof cannot run.

</details>

<details>
<summary>ChatGPT (partial)</summary>

ChatGPT gets this skill through the Codex plugin, which brings the whole ship-pipeline pack. Run the two Codex commands above, then in ChatGPT type `@` and the skill name.

**Limit:** Writes billing code from pasted code; the Stripe CLI webhook test and database proof cannot run.

</details>
<!-- skill-readme:end -->
