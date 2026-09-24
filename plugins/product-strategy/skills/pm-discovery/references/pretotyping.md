# Pretotyping: testing demand before you build

Scope note: this draws on Alberto Savoia's publicly posted pretotyping materials and methodology pages, not a reading of his full book *The Right It*. Treat it as a practical summary of the public method, not a chapter-by-chapter extraction.

## Why pretotype before prototyping
A prototype tests whether something *works*. A pretotype tests whether anyone will actually *engage* with it, before either is fully built. The two questions are different, and confusing them wastes effort — a beautifully working prototype for something nobody wanted is still a failure discovered too late. Choose the method by which question is actually in doubt.

## The core steps
1. Name the single assumption whose failure would sink the idea fastest — test that one first, not the easiest one.
2. Turn a vague belief about demand into a falsifiable **XYZ hypothesis**: "At least X% of Y will do Z." Define the population (Y), the observable behavior (Z), the denominator, the timeframe, and the conditions. Justify the threshold (X%) from the underlying economics, not from whatever number would flatter the result.
3. Pick a reachable test group and be explicit about what it does and doesn't represent — a convenience sample from one channel doesn't speak for the whole market. Recruit at least part of the group from outside the easiest channel (the team's own list, a founder's network) whenever that's feasible; when it genuinely isn't, record the channel bias as an accepted risk in the write-up rather than letting the result read as broader than it is.
4. Build the smallest thing that produces real behavioral evidence: a manually operated ("concierge") service, a simple stand-in, or an honestly described landing page. Build no more than the hypothesis requires — a click, repeated use, and payment are three different sizes of commitment; know which one is being measured.
5. Collect first-hand behavioral data, kept clearly separate from opinions, secondary research, and expressed interest. Enthusiasm is not willingness to pay.
6. Decide pass/fail/inconclusive *before* running the test. Record exposure, who acted, recruitment bias, cost, and exactly what the result does and doesn't prove. A weak result means revising or dropping the idea, not quietly loosening the bar set beforehand.
7. Treat a first cheap signal (a click, a signup, an expressed "yes") as an invitation to run a second, harder test — not as license to build. When the cheap test passes, run a conditional **concierge test**: deliver the result by hand for a defined period, with a person doing manually what the product would eventually automate ("you become the product until you're ready to fire and replace yourself with your actual product" — Ash Maurya, [Give Yourself Permission to Scale](https://ashmaurya.com/blog/give-yourself-permission-to-scale)). A one-off click is weak evidence; watch instead for **repeat use** — do the same people come back and ask again, unprompted, without being re-recruited. Before recommending a build, estimate the ongoing maintenance/support hours the concierge step actually consumed, even at this small scale, and treat that estimate as an explicit go/no-go gate alongside the demand signal itself — a real "yes" that also implies unsustainable hand-holding is not a green light to build.
8. Keep every test truthful and proportionate — no taking money for something undeliverable without disclosure and authorization, no hiding a material limitation, nothing that could genuinely harm someone who encounters it. Publishing, outreach, payment, or anything production-facing needs its own authorization beyond simply designing the test.

## What a result actually tells you
A test group taking action is evidence about that group's behavior under those conditions — not proof of feasibility, unit economics, or demand beyond that group. Keep that distinction explicit, especially against the temptation to read a small positive signal as a green light for full-scale investment.

## Worked example
For a hypothetical scheduling tool, "people said they liked the idea" is weak evidence — saying so costs nothing. A disclosed manual-scheduling trial, a human handling requests behind the scenes, tests whether a defined group actually submits requests and returns. It says nothing about whether the software is buildable, whether acquisition economics work, or whether demand holds outside that group. Don't manufacture a conversion number to fill in what wasn't actually measured.

## Recording the test
Decision it informs; riskiest assumption; XYZ hypothesis; target group and how it was reached; observed behavior and denominator; what was built; threshold and rationale; duration; cost; disclosure/risk notes; observed result; limitations; resulting decision (proceed, change, stop).

## Sources
- [Ash Maurya, "Give Yourself Permission to Scale"](https://ashmaurya.com/blog/give-yourself-permission-to-scale) — the concierge MVP description quoted in step 7 above.
- [Savoia's pretotyping methodology](https://www.pretotyping.org/methodology.html) — the core framework: the minimal experience and the critical assumption it tests.
- [Pretotyping.org resources](https://www.pretotyping.org/resources.html) — public materials tied to *The Right It*.
- [Savoia's original XYZ hypothesis formulation](https://www.pretotyping.org/methodology.html) — states the "X% of Y will do Z" hypothesis format directly.
- [Pretotype planning canvas, hosted by Savoia](https://www.albertosavoia.com/uploads/1/4/0/9/14099067/pretotyping_planning_canvas_by_chris_callaghan.pdf) — useful for seeing how the hypothesis fields are typically laid out; not reproduced here as a template. The canvas itself is credited only to "The Right It," not to any adapter.
