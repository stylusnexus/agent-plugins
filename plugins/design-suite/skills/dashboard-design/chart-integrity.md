# Chart integrity

For charts used in analysis, reports and dashboards. It adds checks to `metrics-and-charts.md`; it does not repeat its rules on zero baselines, direct labels, small multiples, colour roles or colour-vision simulation. Numbers labelled "recommended" are defaults, not standards. This is expert review, not user research.

## 1. Triage every flaw

Tag each finding with exactly one bin:

- Ugly: looks poor, reading is unaffected (clutter, odd fonts).
- Bad: a reader can misread or be misled (truncated bar, wrong chart type, unreadable labels).
- Wrong: the maths or data is incorrect (slices do not sum to 100%, wrong aggregation).

Check: does every chart finding carry one tag?
## 2. Pick the chart by the message

Write the message as one sentence before choosing. Check: is the question written next to each chart?

| Message | Start with | Not as the only view |
|---|---|---|
| Amounts | Sorted bars or dots | Radar, bubble size |
| Distributions | Histogram, density, ECDF, box or strip | Mean alone |
| Proportions | Bars; pie or stack when rules in section 4 hold | Donut with many slices |
| Relationships | Scatter | Dual-axis lines |
| Uncertainty | Labelled intervals, dot counts | Bars with no stated meaning |

## 3. Proportional ink

- Avoid bars on log axes; use dots. If bars are kept, they show ratios, start at one, and the caption says so. Check: any bar on a log axis without that caption is a finding.
- A shaded change from a baseline is fine if the caption says it is a difference. Check: is the baseline named?

## 4. Categories, stacks and pies

- Sort unordered categories by value. Keep natural order for ordered ones (age bands, months). Check: is any order alphabetical only by default?
- Stack bars only when the total means something (counts, revenue) and segments are few. Only the bottom segment is easy to compare. Check: can a reader answer the question without comparing floating segments?
- Pies only for a few slices (recommended: 5 or fewer) of one whole. Check: do slices sum to 100% with no overlapping categories?

## 4a. Intervals and uncertainty

- Say what the interval is: SD, SE or confidence interval, and the level. Check: does the caption name quantity and level?
- Do not judge a difference from whether two intervals overlap. Check: is the interval of the difference shown or stated when significance is claimed?

## 5. Distributions

- Try several bin widths or bandwidths. Check: does the story survive at least three settings (recommended)? Name the setting used.
- Density curves can run into impossible values (negative ages, counts below zero). Check: does any curve extend past the physical limits of the data?
- Skewed data: add an ECDF, or a log axis labelled as log. Check: can a reader read the median and quantiles directly?

## 6. Smoothing and fits

- Disclose the method (moving average, LOESS, spline, fitted formula) and its main setting. Check: is it named in the caption?
- Do not draw a smoothed line or fit beyond the data range. Check: do line ends match the first and last data points?

## 7. Overplotting

- Moderate overlap: partial transparency plus light jitter. Check: can a reader tell dense areas from sparse?
- Very large counts (recommended: above about 10,000 points): 2D bins or hexagons with a count legend.

## 8. Legends and colour

- Legend order matches the visual order of the lines at the right edge. Check: top to bottom, do they agree?
- Qualitative colour ceiling: about 5 or 6 hues (recommended, see `metrics-and-charts.md` section 5); past 8, always use direct labels or panels. Check: count distinct hues.
- Use a colour-blind-safe palette (Okabe-Ito style) and pair colour with shape, line type or label. Check: does a greyscale print still separate every category?
- No rainbow scales. Check: does a sequential scale get steadily lighter or darker in greyscale?

## 9. Compound figures

- Panels carry small lowercase labels (a, b, c) top left so text can cite them.
- Same colour means the same group in every panel. Check: any colour reused for a different group is a finding.
- Align axes across panels that compare; if scales must differ, say so in the caption.

## 10. Captions, tables and marks

- A caption opens with the claim, not "This chart shows". Check: does the first sentence state a finding?
- Table rules: numbers right-aligned with equal decimals, no vertical rules, no lines between data rows, caption above. Check: scan each numeric column.
- No gratuitous 3D (tilted pies, 3D bars). Check: is any depth effect carrying no data?

## 11. Size and export

- Check text at final size: render at the width it will be shown (recommended: 3 to 5 inches for a document column). Check: can axis labels be read there?
- Vector (SVG or PDF) or PNG for charts. Never JPEG, which smears lines and text. Check: file type of every exported chart.

## 12. Reproducibility

- Every chart regenerates from data and code, with seeds fixed for jitter and sampling. Check: does one command rebuild all charts?
- No hand edits in an illustration tool. Check: does the output file differ from a fresh rebuild?

## Report

State what was checked and what was not (for example, data not available to recompute totals). Mark findings VERIFIED or NEEDS-TEST. Never claim a chart is correct, only that no issue was found in the checks listed. Report only; do not change charts unless asked.
