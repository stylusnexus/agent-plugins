# Experiment card

Fill in before looking at any data — see [trustworthy experiments](../references/trustworthy-experiments.md). Changing this card after the experiment starts defeats the point of having one.

## Setup

- **Hypothesis:** [one sentence — what change, what metric, which direction]
- **Primary metric:** [one metric — the one the decision rides on]
- **Baseline rate:** [current value of the primary metric]
- **Smallest effect worth detecting:** [the smallest lift/drop that would actually change what you do]
- **Sample size / running time, fixed in advance:** [computed from a calculator such as Evan Miller's Sample Size Calculator — https://www.evanmiller.org/ab-testing/sample-size.html]
- **Decision rule:** [what result leads to which action — write this now, not after seeing the number]

## Can this actually be randomized?

- **If yes:** [variant split, how it's assigned]
- **If no (pricing change, single-market launch, redesign shipped to everyone):** name the quasi-experiment method instead — difference-in-differences (compare your metric's change against a similar untreated group's change over the same window) or synthetic control (a weighted combination of untreated units built to track yours before the change). Check the "parallel trends" assumption on historical data before trusting either.

## While it's running

- [ ] Not peeked at and stopped early on a good-looking result — the significance math assumes the sample size was fixed in advance
- [ ] Sample ratio checked: does the actual traffic split match what was configured?
- [ ] Only the one primary metric decided above is being used for the decision

## Reading the result

- **Did the metric move immediately and hold, or reverse over time?**
- **Any of the common misreads apply?** (outliers, an underpowered secondary metric read as "no effect," a borderline p-value treated as a win, a novelty effect mistaken for a lasting one, an improbably large win taken at face value instead of checked first — see the reference for the full list)
- **Result vs. the decision rule written above:**

---

## Example (fictional)

Hypothesis: a shorter signup form increases completed signups.
Primary metric: signup completion rate.
Baseline: 24%. Smallest effect worth detecting: 4 points.
Sample size: 1,900 per variant (from Evan Miller's calculator at 80% power, 5% significance).
Decision rule: if completion rate is up ≥4 points and sample ratio is within expected range, ship the shorter form; otherwise keep the current form.
