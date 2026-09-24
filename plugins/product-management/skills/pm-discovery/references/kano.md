# Kano model: how a segment responds to a feature being there or not

Noriaki Kano, Seraku, Takahashi, and Tsuji introduced this model in "Attractive Quality and Must-Be Quality" (*Journal of the Japanese Society for Quality Control*, 1984). It answers one specific question well — how satisfaction responds to an attribute's presence or absence for a defined segment — and complements strategy, value-proposition work, and prioritization rather than replacing any of them.

## The five categories
- **Must-be** — its absence causes strong dissatisfaction, but its presence barely registers as a plus. Table stakes.
- **One-dimensional / performance** — satisfaction rises roughly in proportion to how well the attribute is delivered.
- **Attractive** — its absence isn't noticed or missed, but its presence delights.
- **Indifferent** — the attribute doesn't move satisfaction either way for this segment.
- **Reverse** — this segment prefers the attribute *not* be present.
- **Questionable** — an internally inconsistent response pair; a data-quality flag, not a sixth category.

## The paired-question method
For each clearly scoped attribute, ask a functional question ("how do you feel if this is present?") and a dysfunctional question ("how do you feel if this is absent?"), each with five response options: like, expect/must-have, neutral, can live with, dislike. Classify the pair using the standard cross-tabulation (rows = functional response, columns = dysfunctional response):

| Functional \ Dysfunctional | Like | Expect | Neutral | Live with | Dislike |
|---|---|---|---|---|---|
| Like | Q | A | A | A | O |
| Expect | R | I | I | I | M |
| Neutral | R | I | I | I | M |
| Live with | R | I | I | I | M |
| Dislike | R | R | R | R | Q |

A = attractive, O = one-dimensional, M = must-be, I = indifferent, R = reverse, Q = questionable. This cross-tabulation is the standard convention, documented for example in Atlason & Giacalone, ["Rapid computation and visualization of data from Kano surveys in R"](https://pmc.ncbi.nlm.nih.gov/articles/PMC6263047/) — state the convention explicitly if combining results from a source that lays the table out differently.

## Running it well
1. Ground the exercise in a real decision, segment, and a genuinely well-defined attribute. If there's no survey data yet, help design one — a team's guess at how customers will react is a hypothesis, never a substitute for asking them.
2. Draft one question pair at a time. Example: "If you could export your project as a PDF, how would you feel?" / "If you couldn't export your project as a PDF, how would you feel?" Name any assumed alternative explicitly, and don't bundle unrelated features into one pair or hint at a preferred answer.
3. Pilot the wording for comprehension before fielding it. Record the exact question text, recruitment method, segment, and date. A draft doesn't need authorization to write; sending it to real participants does.
4. Keep every raw paired response and classify each one rather than only reporting a summary. Report the full A/O/M/I/R/Q breakdown, the response count, and any segment split — don't force a majority label through a near-tie, and look into questionable or reverse responses rather than quietly recoding them away.
5. Translate the category into a decision alongside strategic fit, cost, dependencies, and risk — a must-be label doesn't mean every proposed implementation is warranted, and an attractive label doesn't mean "build it next." Kano says nothing about willingness to pay, market size, or whether people will actually adopt the feature once shipped.
6. Revisit periodically. What reads as attractive today can become an expected baseline as a market matures — but there's no fixed schedule for that shift, so check the actual segment rather than assuming it on a timer.

## Producing the deliverable
Deliver either the question set for a study that hasn't run yet, or an evidence-backed classification table for one that has, plus a plain-language recommendation and its limitations. A visual helps but isn't required: prefer Lucid via `pm-visuals`, with Mermaid as the fallback for a simple category map. For the classic satisfaction-curve chart (fulfillment on the horizontal axis, satisfaction on the vertical), label it conceptual rather than fitted to real numbers unless it genuinely is. Avoid placing individual features at precise coordinates without data to justify it — a category table communicates the same information more honestly. Keep reverse and indifferent responses visible in the output rather than dropping them because they're less flattering.

## Before calling it done
Check: no invented respondents or votes; question wording preserved exactly as asked; the cross-tab read in the right orientation; counts that actually reconcile; mixed or split results kept rather than smoothed over; any team hypothesis clearly separated from real survey data; and a prioritization rationale that draws on more than the Kano label alone.
