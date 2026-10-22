# Decision-first layout

## 1. Start from the decision, not the data

Before placing anything, write for each user:

| Field | Example form | Status |
|---|---|---|
| Decision or question | "Is anything needing my action today?" | supplied or MISSING INFORMATION |
| Cadence | each morning, per release, on alert | supplied or MISSING INFORMATION |
| Action it leads to | open, approve, escalate, ignore | |
| Cost of being wrong | missed incident vs. wasted minute | |

If the decision list is empty, stop and ask; a layout without decisions is decoration. Every element on the page must map to a row here. Elements that map to none are candidates to remove or move to detail.

## 2. Three layers

1. Attention: what needs a human now (failing, blocked, awaiting approval, stale beyond tolerance). Top of the page. Empty state says "nothing needs attention" only when every source reported recently (see data-states.md).
2. Summary: the few numbers or statuses that answer the cadence question. Each with its comparison and freshness.
3. Detail: tables, histories, per-item views reached by drill-down. Not shown by default on the first screen.

Rule: the first screen should let the user decide whether to go deeper, without scrolling on the target device if possible.

## 3. Hierarchy

- Order by consequence then urgency, not by system or team structure.
- Use size, position and weight, in that order, to show importance; colour is a supporting cue only.
- Group by the question answered ("Deployments", "Approvals waiting"), not by data source, unless source is the question.
- Put related signals together and the comparison next to the number.
- One primary region. If five regions compete, none is primary.
- Keep placement stable between visits so users learn where things are; do not reorder by live values unless the ordering is the point (a queue sorted by urgency).

## 4. How many top-level numbers

Recommended: about 3 to 6 top-level summary numbers or statuses for a single user and cadence. This is a design guideline, not a measured limit; fewer is better when fewer answer the question. If more seem necessary, check whether:
- some are for a different decision (split into another view or tab);
- some duplicate each other (keep the one that drives action);
- some only matter when abnormal (surface them only when abnormal, in the attention layer).

An aggregate "health score" is allowed only if its inputs and weights are visible and a decision follows from it. Otherwise do not invent one.

## 5. Summary versus detail

| Question | Summary shows | Detail shows |
|---|---|---|
| Is it OK? | status, one number, freshness | history, per-component breakdown |
| Did it change? | delta with baseline | time series, events that explain it |
| What do I do? | the next action link | the records, logs, owner |

Every summary item must be clickable or otherwise lead to its detail and its source. A number with no route to evidence is hard to trust.

## 6. Labels and copy

- Plain words the user already uses; define abbreviations on first use or on hover plus visible text for touch.
- Say what is measured and over what period ("Failed deploys, last 7 days").
- Status words state a fact ("Last report 3 h ago"), not a judgement the system cannot support ("Healthy") unless the criteria are visible.

## 7. Layout mechanics

- Use a consistent grid; align numbers and labels so scanning is easy.
- Cards are fine but avoid nesting boxes inside boxes; spacing and headings can do the grouping.
- In dense views (many numbers), drop the card boxes and separate groups with a hairline divider or space. Keep data unboxed unless raised height has a purpose. Test: a metric row with no borders is still scannable.
- Sans-serif only for dashboards and software UI. Dense does not mean tiny: body at 14px or larger and small labels at 12px or larger (recommended minimums).
- Use the accent colour for one job. Colour that is not the accent is reserved for state (ok, warning, error).
- Provide reading order that matches visual order for keyboard and screen-reader users.
- On narrow screens, keep the attention layer first, stack summary items, move detail behind navigation. Hand dense tables to the mobile design role.

## 8. Existing-dashboard review starter

1. List every element currently shown.
2. Map each to a decision. Mark unmapped elements.
3. Trace each to its source and owner; mark untraceable ones MISSING INFORMATION.
4. Count top-level numbers against the recommended range.
5. Check that the attention layer exists and is truthful when data is missing.
6. Propose the smallest rearrangement that fixes the worst finding first.
