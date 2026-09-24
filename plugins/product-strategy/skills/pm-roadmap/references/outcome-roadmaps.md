# Outcome-based roadmaps

A roadmap is read as a promise even when nobody meant it as one. Two public ideas, used together, are what keep it honest: a format whose columns encode confidence instead of dates, and an explicit line for the rare item that really is a date-bound promise.

## Now / Next / Later encodes confidence, not commitment

ProdPad co-founder Janna Bastow built the Now-Next-Later format after watching detailed, date-based roadmaps mislead the people reading them. In her own account: **Now** holds work the team is actively building, specified enough to execute; **Next** holds what is queued once Now clears, with less detail because it isn't in front of the team yet; **Later** holds the "big boulder blocks" — real problems the team intends to address, with the solution still undefined. She wrote it up after finding "timeline roadmaps aren't effective," and designed the format to be readable in about ten seconds by someone outside the team who has no context to spare. (Janna Bastow, [ProdPad, "Why I Invented the Now-Next-Later Roadmap,"](https://www.prodpad.com/blog/invented-now-next-later-roadmap/) 2022-10-18.)

The shrinking detail from Now to Later is not a defect to fix by filling in more — it is the format doing its job. A "Later" item with the same specificity as a "Now" item is a false signal: it claims a certainty about scope and sequencing that discovery hasn't earned yet. *Product Roadmaps Relaunched* (C. Todd Lombardo, Bruce McCarthy, Evan Ryan, and Michael Connors, O'Reilly, 2017-10-25) is a fuller public treatment of the same problem — its subtitle, *How to Set Direction while Embracing Uncertainty*, names the trade-off directly: a roadmap has to give real direction while admitting how much of the far end is still unknown.

## When a commitment really is a commitment

Some roadmap items are not confidence bands — they are fixed-date promises the business has already made externally: a trade-show launch, a contractual partner date, a regulatory deadline. Marty Cagan calls these **high-integrity commitments**, and they are deliberately rare. Cagan's own warning is the operative constraint: "high-integrity commitments and deliverables should be the exception and not the rule. Otherwise it is a slippery slope and pretty soon your objectives are nothing more than a list of deliverables and dates, which is little more than a reformatted roadmap." (Marty Cagan, [SVPG, "Team Objectives – Commitments,"](https://www.svpg.com/team-objectives-commitments/) 2020-03-04.) A commitment made this way should follow, not precede, enough discovery to know the solution is valuable, usable, feasible, and viable — see [product risk](../../pm-discovery/references/product-risks.md) for that check.

## Putting the two together

Mark every roadmap item with one of two states: a *confidence band* (Now/Next/Later, evidence still accumulating, scope expected to change) or a *high-integrity commitment* (a specific date, made deliberately, rare). Mixing the two without saying which is which is what turns a roadmap into a false promise — a "Later" item and a contractual date look identical on a slide unless the roadmap says otherwise.

Use the [outcome roadmap working sheet](../templates/outcome-roadmap.md) to draft this: it carries the Now/Next/Later horizons, a separate **Dates and commitments** table for anything that has crossed into high-integrity territory, and a review record for what changed the sequencing and why. Populate a first draft from real project material, state evidence status per row, and work through the most consequential gap with the user rather than requiring every cell filled before it's useful.
