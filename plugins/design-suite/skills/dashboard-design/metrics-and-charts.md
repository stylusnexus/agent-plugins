# Metrics, numbers and charts

Values labelled "recommended" are design defaults, not standards. Confirm them with the owner of the data.

## 1. Numbers

- Say what is counted, over what period, for what scope. Label beside the number.
- Units always visible: %, ms, GB, USD. Currency code or symbol and whether tax is included.
- Format for scanning: thousands separators, consistent decimals per column, right-align numeric columns so digits line up, tabular figures where the font supports them.
- Precision: only as many digits as are meaningful. Do not show 12.3846 when the source is rounded.
- Large values: abbreviate (12.4k) only when the exact value is available on drill-down or hover plus visible alternative; never mix abbreviation styles on one screen.
- Percentages: state the denominator; a percent of a tiny count misleads, so show counts alongside.
- Dates and times: unambiguous (2026-10-21 or 21 Oct 2026), with time zone when time matters. Relative time plus absolute.
- Negative and zero: zero is a value; distinguish from missing (see data-states.md).
- Localise number and date formats to the user's locale where the product supports it.

## 2. Deltas and baselines

A change without a baseline means nothing. Always state "versus what":
- previous period (last 7 days vs. the 7 before),
- same period last cycle (for seasonality),
- target or threshold (only if supplied),
- a named reference.

Rules: show absolute and relative change together when the base is small; mark direction with arrow plus sign and text, not colour alone; do not colour every increase green (more errors is up and bad); show the compared periods explicitly; say when the comparison period is incomplete or partial.

## 3. Choosing a chart by question

| Question | Usually works | Avoid |
|---|---|---|
| How much right now? | Single number with comparison; bullet bar | Gauge or dial (poor space use, hard to read precisely) |
| How does it change over time? | Line chart (continuous), column chart (discrete periods) | 3D, area stacks with many series |
| How do categories compare? | Horizontal bar, sorted | Pie with many slices; radar |
| Part of a whole? | Stacked bar, or a table; pie only for few slices that sum to a clear whole | Donut with 8 slices |
| Distribution? | Histogram, box plot | Average alone |
| Relationship of two variables? | Scatter | Dual-axis lines |
| Rank or exact lookup? | Table | Chart that forces reading values off an axis |
| Status of many items? | Table with status column, small multiples | One colour-coded grid with no legend |

If no decision depends on the chart, remove it. If a sentence or a table states the answer more clearly, use that.

## 4. Axes and baselines

- Bar and column charts start at zero; length encodes value. Truncating them exaggerates differences.
- Line charts may use a non-zero baseline when the change matters more than the absolute level, but label the axis clearly and say if it is truncated.
- Never use a broken axis silently; avoid dual axes (readers infer a relationship that is not there). Use two aligned charts instead.
- Label axes with units; label lines directly rather than relying only on a legend where possible.
- Keep scale consistent across charts that are compared; same scale for small multiples.
- Log scales only for audiences who read them, labelled as log.
- Show gaps in data as gaps (broken line), not interpolated or zero.
- Include threshold or target lines only if supplied.

## 5. Colour

- Use colour to encode, not decorate. Few categories: up to about 5 or 6 distinguishable hues (recommended); beyond that group or filter.
- Do not rely on colour alone: add direct labels, patterns, markers or position.
- Meet WCAG 2.2 contrast: 3:1 for graphical objects that convey information, 4.5:1 for text (1.4.11, 1.4.3).
- Keep status colours consistent everywhere and reserved for status.
- Sequential palettes for ordered magnitude, diverging only around a meaningful midpoint, categorical for unordered groups.
- Check light and dark themes and colour-vision-deficiency simulations.
- Use the product's existing tokens; no new palette or design system unless requested.
- Tinted badge fills with darker same-hue text can pass. Worked example (checked on one sample set; recompute on the project's real colours): red 6.26, green 6.08, yellow 4.62 and blue 4.98 to 1, all at or above 4.5. Verify every real pair.

## 6. Tables versus charts

Use a table when users look up exact values, compare many attributes, or act on rows. Use a chart when the shape (trend, outlier, comparison) is the point. Often both: chart for the pattern, table for the records. Table rules: sticky header, sortable on columns that make sense, default sort by consequence, one row per entity, row actions explicit, readable on narrow screens (see mobile-design).

## 7. Filters and time ranges

- Default to the range that matches the cadence (supplied or MISSING INFORMATION).
- Show the active range and filters on the page itself, including in anything exported or shared.
- Offer a few presets (recommended: last 24 hours, 7 days, 30 days) plus custom range; remember the choice only if it will not mislead the next visit.
- Make filter changes reversible: "Clear all", and visible count of active filters.
- Zero results after filtering is an empty state that says which filter caused it.
- Time ranges state whether the current period is partial and what time zone applies.
- Apply filters consistently to every widget they claim to affect; mark widgets they do not affect.

## 8. Drill-down

- Every summary leads to its detail in one step, preserving filters and range.
- Breadcrumb or back path to the summary; keep scroll and filter state on return.
- Detail ends at the source record or a link to the owning system. Read-only surfaces link out rather than editing authoritative data.
- Hover-only detail has a tap and keyboard equivalent.
- Chart accessibility: provide a text summary or data table alternative, keyboard-reachable data points where interactive, and do not convey meaning by colour only.
