# Assessing and responding to product risk

Two separate questions get run together when teams talk about "risk": what kind of risk is this, and what should we do about it now that we've named it. Keep them separate — the categorization tells you who is closest to the evidence; the response tells you what actually changes as a result of naming it.

## What kind of risk is this

Marty Cagan's four-risk framework names the questions a team needs answered before it ships anything: value risk — "whether customers will buy it or users will choose to use it"; usability risk — "whether users can figure out how to use it"; feasibility risk — "whether our engineers can build what we need with the time, skills and technology we have"; and business viability risk — "whether this solution also works for the various aspects of our business." Cagan's own elaboration of viability is broader than pricing: it spans go-to-market fit, sales-channel compatibility, legal and partner compliance, customer-acquisition cost, monetization mechanics, and brand consistency — any one of which can kill a solution that is otherwise valuable, usable, and feasible. (Marty Cagan, [SVPG, "The Four Big Risks"](https://www.svpg.com/four-big-risks/), 2017-12-04.)

Treat this as a checklist to re-run per bet, not a one-time audit: a solution that clears value and usability risk in discovery can still fail on feasibility once engineering scopes it, or on viability once legal or finance reviews it. Route each identified risk to whoever is closest to the relevant evidence — usually product for value and viability, design for usability, engineering for feasibility — but that is "who investigates first," not "who alone may raise it." Anyone on the team can flag a risk in any category.

## What to do about it

Once a risk is named, respond to it on purpose instead of defaulting to "build it and see." Wissam Yaacoub's PMI Lebanon Chapter presentation gives five deliberate responses for a risk you would rather not have (a threat), including *Escalate*. (Wissam Yaacoub, PMP, PMI-RMP, ["The Know Unknowns: Importance of Project Risk Management (PRM)"](https://www.pmi.org/-/media/pmi/chapters/lebanon-chapter/pdf-and-ppt/march-2019-importance-of-project-risk.pdf), PMI Lebanon Chapter, March 2019 (per URL).) For a risk you could turn to advantage (an opportunity), David Hillson's PMI-published paper builds the positive equivalent of the original four threat strategies (avoid, transfer, mitigate, accept) — it gives four opportunity responses and has no counterpart to *Escalate*. (David Hillson, ["Effective Strategies for Exploiting Opportunities,"](https://www.pmi.org/learning/library/effective-strategies-exploiting-opportunities-7947) Project Management Institute Annual Seminars & Symposium, Nashville, TN, 2001-11-01 — pmi.org blocks automated fetches of this page; an [archived copy](http://web.archive.org/web/20251015183832/https://www.pmi.org/learning/library/effective-strategies-exploiting-opportunities-7947) is fetchable.)

| For a threat | For an opportunity |
|---|---|
| **Avoid** — change the plan so the risk can't occur | **Exploit** — "removing the uncertainty by seeking to make the opportunity definitely happen" |
| **Transfer** — shift the consequence to someone better placed to carry it | **Share** — "passing ownership to a third party best able to manage the opportunity and maximize the chance of it happening" |
| **Mitigate** — reduce its probability or impact | **Enhance** — "increasing its probability and/or impact to maximize the benefit to the project" |
| **Accept** — proceed with eyes open, with or without a contingency reserve | **Ignore** — leave it in the baseline, "adopting a reactive approach without taking explicit actions" |
| **Escalate** — hand a risk outside the team's own authority up to whoever can actually decide on it | *(no opportunity equivalent in this source)* |

Applied to product risk, this reframes discovery from "is this risky" to "what changes because of it." A usability risk you *mitigate* with a design change is a different decision from one you *accept* and monitor after launch. A viability risk you *transfer* — a partner absorbs the compliance burden — is a different decision from one you *avoid* outright by not shipping the feature that carries it, or one you *escalate* because the call sits above the team's own authority. On the opportunity side, a distribution partnership you could *exploit* by committing early is a different decision from one you *share* by giving a partner first crack at it. "Reduce it and hope" is not on this list; pick one response, state the evidence for and against it, and name who is accountable for the choice.

## Recording the decision

For each material risk, capture: which of the four kinds it is, its evidence status (**evidence-backed** / **hypothesis** / **accepted**, per [shared principles](../../product-manager/references/principles.md)), the chosen response and the reasoning behind it, the owner, and what would change the decision later. A risk with no chosen response has not stayed open — it has defaulted to *accept*, whether or not anyone said so out loud. Surfacing that default explicitly is often the most useful thing this exercise does.
