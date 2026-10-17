# Question router

Two decisions, in order: what kind of question is this, and once you know the answer, what's the clearest way to show it.

## Route the question first

Gartner's analytics maturity model names four types of question, and each needs a different kind of answer (Source: Gartner's model, as described in Digital.ai, "IT Decision-Making Through the Lens of Gartner's Analytics Maturity Model," https://digital.ai/catalyst-blog/it-decision-making-through-the-lens-of-gartners-analytics-maturity-model/ — Gartner's own site returns 403 to a direct fetch):

- **Descriptive — what happened.** "How many signups did we get last week?" Answered by reading the number, not by testing anything.
- **Diagnostic — why it happened.** "Why did signups drop?" Answered by segmenting the descriptive number (by channel, by day, by cohort) until the drop traces to something specific.
- **Predictive — what will happen.** "Will this trend continue?" Answered from a trend line or a rate, held to the same honesty about small samples as anywhere else in this skill — a two-week trend from a pre-launch product is not a forecast.
- **Prescriptive — what to do about it.** "Should we double down on this channel?" The only one of the four that should change a plan, and it should rest on a diagnostic answer, not a descriptive one.

Skipping straight from descriptive to prescriptive — "signups dropped, let's try a new channel" — is the most common way a real cause goes unaddressed. Answer descriptive, then diagnostic, before a prescriptive answer gets trusted.

## Then pick the chart

Once you know what you're showing, match it to the chart, not the other way round. The UK Government Analysis Function's guidance on chart selection ([Data visualisation: charts](https://analysisfunction.civilservice.gov.uk/policy-store/data-visualisation-charts/)) states the test plainly: "If you cannot write down the message your chart is giving in a few sentences, you should think again about the chart." Its Financial Times-derived reference table sorts chart types by the relationship being shown — comparison, distribution, time series, ranking, deviation — rather than by how many series happen to fit on a page.

For a straight comparison between categories, prefer a bar chart over a pie chart. Stephen Few's Perceptual Edge newsletter, ["Save the Pies for Dessert"](https://www.perceptualedge.com/articles/visual_business_intelligence/save_the_pies_for_dessert.pdf), calls the pie chart "by far the least effective" of the graphs in common use, because judging a slice's size accurately only works near the 0/25/50/75/100% marks — a bar graph's scale reads correctly at any value. The UK Government Analysis Function's own pie-chart rule is narrower than "avoid pie charts entirely": use one only when there are five categories or fewer, and label the categories directly instead of relying on a separate legend.

For change over time, both sources converge on the line chart. Datawrapper's guide to choosing a chart type ([A friendly guide to choosing a chart type](https://www.datawrapper.de/blog/chart-types-guide)) frames the choice around the chart's job rather than the data type — "depending on your data and your goal, there are always lots of chart types you can simply ignore" — and calls the line chart "intuitive to read and usually a solid choice" for showing developments over time. The UK guidance adds two mechanical rules worth keeping: label lines directly instead of using a legend where the chart allows it, and avoid dual-axis charts where possible — the Analysis Function's stated reason is that "they can be easily misinterpreted" and "the way we display lines in relation to each other can manipulate the data story, even if it is not intentional," and its own alternative is to give each dataset its own chart with its own y-axis, with clear annotations, rather than merging both onto one.

For a bar chart specifically, the UK guidance holds the numeric axis to zero — "breaking the numerical axis... is when you make the axis start from a number other than zero," which it treats as a bar-chart-specific distortion, not a rule for every chart type — and keeps the gap between bars narrower than a single bar's width, ranked by value unless the categories have a natural order of their own (months, funnel stages).

None of this is a fixed widget count or a template to fill mechanically. Start from the message in one sentence, then choose the chart that makes that sentence obvious at a glance.
