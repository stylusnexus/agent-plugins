# Product Strategy Canvas

**Product:**
**Prepared with:**
**Date:**
**Status:** Draft — assumptions still open · Accepted — team is committing to these choices

## What this is
A one-page view of the strategy choice cascade from Roger Martin and A.G. Lafley's *Playing to Win: How Strategy Really Works* — five integrated choices, not five separate boxes: winning aspiration, where to play, how to win, capabilities, and management systems. Each choice constrains, and is constrained by, the others; filling one box in isolation produces a wish list, not a strategy.

Public grounding for the five choices and the quotes below: Roger Martin, ["Decoding the Strategy Choice Cascade"](https://rogermartin.medium.com/decoding-the-strategy-choice-cascade-475d40555eb1); Lenny Rachitsky's "Some takeaways" episode summary of Roger Martin's account, in ["5 essential questions to craft a winning strategy | Roger Martin (author, advisor, speaker)" (*Lenny's Podcast*, 2024-07-25)](https://www.lennysnewsletter.com/p/the-ultimate-guide-to-strategy-roger-martin). This canvas is an original table layout built around those five public choices — it does not reproduce anyone's proprietary template, and it is not the Blue Ocean strategy canvas, the Strategyzer Value Proposition Canvas, or the Business Model Canvas (see [sources](../../product-manager/references/sources.md) for those as further reading).

Mark every answer with its evidence status:
- **evidence-backed** — grounded in real data, interviews, or usage you can point to
- **hypothesis** — the team's best current guess, not yet tested
- **accepted** — a committed choice the team is holding itself to, whether or not it is proven

## 1. Winning aspiration
*What does winning look like, and for whom? "What is our winning aspiration? Clarify what you aim to achieve with your strategy. This guides all subsequent decisions and actions toward a clear objective."*

| Question | Answer | Evidence status |
|---|---|---|
| What would winning mean for our customers? | | |
| What would winning mean for us (the business or project)? | | |
| Why this aspiration, and not a bigger or smaller one? | | |

## 2. Where to play
*Which customers, segments, geographies, or use cases will we compete in — and, as important, which will we deliberately not? "Select specific markets, segments, or niches where you will compete. Focus is crucial; trying to be everywhere can dilute effectiveness."*

| Question | Answer | Evidence status |
|---|---|---|
| Which segment(s) are we choosing? | | |
| Which segments are we deliberately NOT playing in, and why? | | |
| What has to be true about this arena for the aspiration above to be reachable? | | |
| Is there real room to price here — what would a customer in this segment actually pay, and does that hold up once seasonality or cohort differences (early adopters vs. later, one region vs. another) are accounted for? | | |
| **The main strategic fork:** name the single biggest either/or choice this "where to play" answer locks in — the future we're walking away from by choosing this one. | | |

## 3. How to win
*What is the basis of advantage in the chosen arena? "You must either offer customers superior value or operate at a lower cost than competitors in your chosen areas" — if you're neither, competitors can "bully" you.*

| Question | Answer | Evidence status |
|---|---|---|
| Superior value, lower cost, or a specific combination — and why? | | |
| What do we do differently from the alternatives customers use today? | | |
| Who could copy this, and why wouldn't they? | | |

Any competitor fact used above — a price, a feature claim, whether a named competitor's product still exists at all — needs to be checked now, not carried forward from memory or an old note. Flag anything not verified today as unverified rather than stating it as current fact; competitor pricing and lineups change fast enough that a stale fact reads as a current one if left unmarked.

Route the detailed customer-value reasoning behind this box to `pm-value-proposition`.

## 4. Capabilities
*What must we be able to do — distinctively — to win the way we've chosen? Capabilities here means "distinctive strengths that set you apart from competitors," not a generic list of things any competent team can do.*

| Capability needed | Do we have it today? | Build / buy / partner | Evidence status |
|---|---|---|---|
| | | | |

Route a full current-vs-target capability map, with gaps and dependencies, to `pm-capabilities`.

## 5. Management systems
*What systems, processes, and measures keep the capabilities and the strategy alive day to day, rather than bolted on after the fact? "What management systems are required to ensure the capabilities are in place? Put in place supportive systems and processes to sustain your capabilities over time…"*

| System or process | What it needs to reinforce (which capability / how-to-win choice above) | Evidence status |
|---|---|---|
| | | |

## Key measures and open assumptions
*This section is this plugin's own addition, not part of the cited framework — it exists to connect the cascade above to the rest of this plugin's workflow.*

**Measures that tell us this is working.** Route to `pm-objectives` for full definitions (numerator/denominator, baseline, target, owner, review cadence).

| Measure | What it tells us | Baseline | Evidence status |
|---|---|---|---|
| | | | |

**Assumptions that would break this strategy if wrong.** Route to `pm-discovery` for the cheapest test of each. Always include one row testing whether the product actually has the capabilities this strategy relies on today — not just whether the team could plausibly build them.

| Assumption | What breaks if it's false | Cheapest test | Evidence status |
|---|---|---|---|
| The product actually has the capabilities section 4 (Capabilities) claims, today | Everything downstream of "how to win" is aspirational, not real | Check the claimed capability against what's actually shipped and working now, not what's planned | |
| | | | |

## Fit checks before calling this done
1. Who could copy this, and why wouldn't they? For the full defensibility check, route to `pm-strategy-fit`.
2. Do the five choices above reinforce each other, or do any two quietly fight (a where-to-play choice that needs a capability the how-to-win box never funds, a management system that measures the wrong thing)? Go choice by choice, not just at a glance — name the specific pair that conflicts, if any, rather than concluding "looks fine" without checking each combination.
3. What has to be true for this to work, and what's the cheapest way to find out?
4. Say the main strategic fork out loud: what's the single biggest either/or this canvas has actually decided, and what future does choosing it close off? A canvas that doesn't name a real fork is often listing options rather than committing to one.

A filled canvas is a compressed hypothesis set, not a validated strategy.

---
*Framework: Roger Martin & A.G. Lafley's "Playing to Win" strategy choice cascade, from public sources cited above. Table design, evidence-status labels, and the measures/assumptions section are this plugin's own addition. See [sources](../../product-manager/references/sources.md) for the full strategy reading list and its limits.*
