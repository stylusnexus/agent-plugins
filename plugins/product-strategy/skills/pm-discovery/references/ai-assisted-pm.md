# Where AI assistance helps in product work, and where it doesn't

An AI assistant working through this suite is a drafting and synthesis tool operating on evidence someone else gathered — it is not a source of evidence itself. That line is worth stating up front because it's the one AI assistance blurs fastest.

## A risk-management frame, not a task list

NIST's AI Risk Management Framework organizes AI risk into four functions rather than a fixed list of use cases: **govern** (set accountability for how AI is used before using it), **map** (identify where a given use could go wrong), **measure** (check whether it actually did), and **manage** (act on what measurement finds) (NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), NIST AI 100-1, January 2023) — intended, per NIST's own AI RMF landing page, "to improve the ability to incorporate trustworthiness considerations into the design, development, use, and evaluation of AI products, services, and systems." ([nist.gov/itl/ai-risk-management-framework](https://www.nist.gov/itl/ai-risk-management-framework).) Applied here, that means judging each use of AI assistance in this suite by where it sits in the workflow and what checking it needs — not by whether "AI use" in general is acceptable.

**Govern:** the [shared principles](../../product-manager/references/principles.md) already set the accountability line — ground recommendations in supplied research and actual context, label evidence versus inference versus hypothesis, and never let a drafted artifact stand in for a decision the user hasn't made. That governs every use below.

**Map, by stage of work:**
- *Structuring a messy problem* — turning a rough discovery brief into candidate job steps, risk categories, or roadmap horizons to react to. Low risk: the user is the one who judges whether the structure fits their actual situation.
- *Synthesizing supplied evidence* — summarizing interview notes, support tickets, or survey exports the user has provided into themes. Medium risk: a summary can quietly drop a contradictory data point or an outlier that mattered; the source material stays available for the user to check against.
- *Populating a working sheet or roadmap* — drafting a first pass at the value proposition worksheet, an outcome roadmap, or a risk table from real project material. Medium-high risk: this is where a plausible-sounding but unsupported row is most tempting to write, because the template has a blank waiting for it.
- *Generating evidence itself* — interview transcripts, personas, survey responses, or market data with no real source behind them. Out of scope for this suite regardless of framing; see `synthetic_research` in [insight sources](insight-sources.md) for the one place simulated material belongs, and even there it is never presented as customer evidence.

**Measure and manage** happen the same way for every stage above: verify claims against their source before they're used.

## How to verify, not just when

Anthropic's own guidance on reducing hallucinations gives three checks worth applying to anything this suite drafts: let the assistant say it doesn't know rather than filling a gap; ground claims in direct quotes from the actual source material rather than paraphrasing from memory; and, for anything presented as a finding, require a supporting quote for each claim — "if it can't find a quote, it must retract the claim." ([Claude Docs, "Reduce hallucinations,"](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations).) The same discipline this suite already asks of its own reference files — a claim traces to a fetched source or it doesn't get made — applies to what an AI assistant hands back inside a working session.

## What doesn't change

Drafting, synthesizing, and structuring do not authorize sending outreach, publishing content, or committing to a roadmap date on the user's behalf. Every artifact an AI assistant produces here carries the same **evidence-backed** / **hypothesis** / **accepted** labeling as anything else in this suite, and a fluent draft is not evidence that the thing it describes is true.
