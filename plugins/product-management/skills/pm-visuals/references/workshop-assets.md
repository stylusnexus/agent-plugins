# Stylus Nexus workshop assets

Eight reusable visuals for product conversations, workshops and reports. The
diagrams use editable vector objects rather than screenshots of research PDFs.
Copy the needed asset into the project, add its scope/date/evidence, and inspect
the result before sharing it. Blank working fields are prompts, not findings.

- [Editable PowerPoint deck](../assets/workshop-toolkit.pptx)
- [Printable eight-page PDF](../assets/workshop-toolkit.pdf)

| Asset | Use it to | Editable SVG | Printable PDF |
|---|---|---|---|
| Pareto analysis | Explore concentration in measured categories; includes fictional example data | [SVG](../assets/pareto-analysis.svg) | [PDF](../assets/pareto-analysis.pdf) |
| Porter's Five Forces | Discuss competitive pressure within a defined industry | [SVG](../assets/five-forces.svg) | [PDF](../assets/five-forces.pdf) |
| Outcome roadmap | Sequence outcomes and learning in Now / Next / Later horizons | [SVG](../assets/outcome-roadmap.svg) | [PDF](../assets/outcome-roadmap.pdf) |
| Value curve | Compare offerings on explicitly defined factors and scales | [SVG](../assets/value-curve.svg) | [PDF](../assets/value-curve.pdf) |
| Assumption map | Identify consequential claims with weak evidence and choose tests | [SVG](../assets/assumption-map.svg) | [PDF](../assets/assumption-map.pdf) |
| Customer journey | Connect customer steps, friction, evidence and opportunities | [SVG](../assets/customer-journey.svg) | [PDF](../assets/customer-journey.pdf) |
| Product Strategy Canvas | Relate strategic choices, trade-offs and unresolved questions | [SVG](../assets/strategy-canvas.svg) | [PDF](../assets/strategy-canvas.pdf) |
| Value proposition | Connect a customer job to mechanisms, benefits and supporting evidence | [SVG](../assets/value-proposition.svg) | [PDF](../assets/value-proposition.pdf) |

## Edit and regenerate

Edit text and shapes directly in the PPTX or SVG. The PDF is the printable
companion, not an editable form. These working assets complement the more
detailed Markdown worksheets in `pm-canvas`, `pm-value-proposition`,
`pm-roadmap`, and `pm-discovery`.

Optional regeneration uses Python with the dependencies in
[requirements-assets.txt](../scripts/requirements-assets.txt). Run from the
`pm-visuals` skill directory:

```sh
python3 scripts/build_workshop_assets.py --output /path/to/project/workshop-assets
```

For a new Pareto example, copy [the CSV](../assets/pareto-fictional-data.csv),
replace its five category/count rows, and add `--pareto-csv /path/to/data.csv`.
This compact template accepts five positive finite counts and short labels;
it sorts categories and recalculates cumulative percentages. Adapt the generator
for a different category count rather than silently dropping observations. The
bundled example remains explicitly fictional.

When using actual data, identify the measure and context explicitly:

```sh
python3 scripts/build_workshop_assets.py --output /path/to/project/workshop-assets \
  --pareto-csv /path/to/data.csv --pareto-status supplied \
  --pareto-unit "Cost (USD)" --pareto-context "September support costs"
```

Use unique, nonempty category names. `supplied` labels the dataset as user-supplied,
not independently verified; it does not establish data quality. The numeric CSV
column remains `count` for compatibility with the template even when its measure
is cost or time. The unit label specifies its meaning.

The generator is the editable source for consistent multi-format exports. It
does not import changes made manually to exported slides or SVGs. Use a separate
output directory when regenerating so project edits are not overwritten.

## Evidence and interpretation

Pareto bars use a single unit across categories; the cumulative line uses percent
of the total. Replace the fictional data before making product claims. Select
frequency, cost, time or another defensible measure deliberately: the most common
problem may not be the most consequential. Do not infer an 80/20 split or causality.
See [ASQ's method reference](https://asq.org/quality-resources/pareto).

Five Forces describes rivalry, entry, substitutes, supplier power and buyer power.
Record actual industry evidence and uncertainty rather than treating the blank
diagram as an assessment. Framework credit: Michael E. Porter; see
[Harvard Business School](https://www.isc.hbs.edu/strategy/business-strategy/Pages/the-five-forces.aspx).

Value-curve scores require a declared scale and evidence. Assumption-map positions
are discussion aids, not measured probabilities. Roadmap horizons are not dates.
Journey maps require observed or explicitly hypothetical customer behavior.

## Attribution

The first six layouts are original Stylus Nexus illustrations of established
methods, distributed under MIT. The strategy-canvas and value-proposition assets
adapt the attributed templates already in this pack and retain CC BY-SA 4.0.
Their license and source credits travel with the SVG, PDF and slide. The combined
deck and PDF contain both kinds of material; do not remove page-level notices.
See the [third-party notices](../../../THIRD-PARTY-NOTICES.md) for sources and
changes. Original downloaded artwork and article PDFs are not included.

The [asset manifest](../assets/manifest.json) records per-asset licenses, sources,
output names and page order. PowerPoint speaker notes carry the same provenance.
