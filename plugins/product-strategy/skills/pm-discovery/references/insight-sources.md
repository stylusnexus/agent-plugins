# Discovery sources and the evidence digest

No single source of evidence is enough on its own, because each one has a different blind spot. Nielsen Norman Group's framing of triangulation is the operating principle here: "the practice of using multiple sources of data or multiple approaches to analyzing data, to enhance the credibility of a research study" — quantitative sources show scale and pattern, qualitative sources show the why underneath them, and "the more significant the decision, the more it pays to triangulate before making it." ([Kathryn Whitenton, NN/g, "Triangulation: Get Better Research Results by Using Multiple UX Methods,"](https://www.nngroup.com/articles/triangulation-better-research-results-using-multiple-ux-methods/) 2021-02-21.)

## Source groups

This suite groups sources by where the signal originates, not by method family — a support ticket and a sales-call note are both "what people say" even though one is written and one is transcribed.

**What people say (self-reported):**
- `customer_interview` — a structured or semi-structured conversation with a job executor; see [research interviews](research-interviews.md).
- `sales_call_note` — what a prospect said unprompted, while trying to decide whether to buy.
- `support_ticket` — what an existing user said while something was already going wrong; biased toward friction, not representative of the whole base.
- `survey` — self-reported, structured, at scale; strong on prevalence, weak on why.

**What people do (behavioral):**
- `product_analytics` — observed usage in the product itself.
- `usability_test` — observed task performance in a controlled setting.
- `site_search_log` — what people typed when the product's own navigation didn't answer their question; a wanted-but-missing signal, not a preference signal.
- `experiment` — observed behavior under a deliberate variant; see [A/B testing](ab-testing.md).

**What the market shows (external):**
- `app_store_review` — self-selected and skewed toward strong reactions, still a real signal at volume.
- `competitor_product` — what alternatives actually do today, not their marketing claims about it.

**What we generate ourselves:**
- `synthetic_research` — AI-generated or simulated material (personas, synthetic interview transcripts, LLM-drafted survey responses). Useful for stress-testing a hypothesis or a discussion guide before real fieldwork; never a substitute for it, and never presented as if it were customer evidence. See [shared principles](../../product-manager/references/principles.md): do not simulate users and present the simulation as research.

Unused source types are options for this project's context, not a mandatory checklist — a pre-revenue product has no support-ticket history yet, and that's a gap to name, not a step to fake.

## The evidence digest

`../../scripts/discovery_digest.py` reads a local JSONL file — one evidence record per line, each with `id`, `source_type` (one of the groups above), `status` (`observation`, `reported`, `inference`, `hypothesis`, or `synthetic`), and `summary`, plus optional `source_ref`, `date`, `segment`, and `theme` — and renders a traceable Markdown table with per-source counts and review flags for missing provenance. It runs entirely locally: no network calls, no writes back to the input file, and no judgment about evidence quality. `synthetic_research` records must carry `status: synthetic`; the script rejects a synthetic record trying to pass as an `observation`, but it cannot detect mislabeled AI text on its own — that check is still human work.

Run it against a discovery evidence file with:
```
python3 scripts/discovery_digest.py path/to/evidence.jsonl
```

Counts describe submitted records, not unique people, real-world prevalence, or validated findings. Treat the digest as a provenance check that makes synthesis possible, not as the synthesis itself — source independence, recruitment bias, and contradictory reports across records still need a human read.
