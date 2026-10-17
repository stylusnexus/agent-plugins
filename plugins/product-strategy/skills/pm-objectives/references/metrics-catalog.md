# Product metrics reference

A working set of 40 standard product and SaaS metrics, grouped by where they sit in the
customer/revenue journey. These are widely published industry conventions, not proprietary
formulas — sources are named per metric below where one originator is credited (Reichheld's
NPS, Dixon/Freeman/Toman's CES, Ellis's PMF survey, the DORA/*Accelerate* delivery metrics);
the rest (CAC, MRR, retention, stickiness, and similar) are common analytics vocabulary with no
single owner. Pull definitions with the plugin's `scripts/metrics_lookup.py` rather than
scanning the table by hand for a large catalog.

Every metric needs, at minimum, the same six things nailed down before it goes on a dashboard:
the qualifying event, the eligible population, the time window, the exact formula, the data
source, and an owner. Skipping any one of those is how two teams end up reporting different
numbers under the same metric name. Finance-facing metrics (MRR, ARR, gross margin) additionally
need reconciliation against the organization's actual accounting policy — this reference is not
accounting guidance.

Select metrics for the decision at hand. A dashboard with all 40 numbers on it teaches nothing;
two or three, chosen because they answer a real question this cycle, do.

## Awareness & Acquisition

| ID | Metric | Definition | Caution |
|---|---|---|---|
| ACQ-1 | Unique Visitors | Distinct people reaching a defined marketing or product surface within a period. | Deduplicate across devices carefully; bot/crawler traffic looks identical to real interest until filtered. |
| ACQ-2 | Visitor-to-Signup Rate | Signups ÷ unique visitors, same window and cohort. | State the attribution window; a late signup still counting toward an early visit changes the rate. |
| ACQ-3 | Customer Acquisition Cost (CAC) | Fully loaded acquisition spend ÷ new customers acquired in the same period. | Partial loading (excluding salaries/tooling) makes CAC look better than reality and breaks comparisons. |
| ACQ-4 | Cost per Lead (CPL) | Acquisition spend ÷ marketing-qualified leads generated. | A cheap lead that never converts is not evidence of efficiency; pair with downstream conversion. |
| ACQ-5 | Channel Mix | Share of new signups or revenue attributed to each channel under one stated attribution model. | Last-click, first-click and multi-touch models assign the same conversion differently; name the model. |
| ACQ-6 | Click-Through Rate (CTR) | Clicks on a placement ÷ impressions of that placement. | High CTR on a misleading placement can hurt everything downstream; read it with post-click conversion. |

## Activation

| ID | Metric | Definition | Caution |
|---|---|---|---|
| ACT-1 | Activation Rate | New users reaching a defined first-value milestone ÷ new users who signed up, within a set window. | Validate the milestone against real retention data; an arbitrary action is not automatically meaningful. |
| ACT-2 | Time-to-First-Value (TTFV) | Elapsed time from signup to the first value milestone, as a distribution. | An average hides users who never reach it; report the non-reaching share separately. |
| ACT-3 | Onboarding Completion Rate | Users finishing every required onboarding step ÷ users who started it. | Completion is not value achieved; a user can finish and still not understand the product. |
| ACT-4 | Aha-Moment Reach Rate | Share of new users performing the action cohort analysis shows correlates with later retention. | The action must come from this product's own retention data, not a borrowed case study. |
| ACT-5 | Product-Qualified Lead (PQL) Rate | Free/trial users meeting a documented usage threshold ÷ all free/trial users. | A usage threshold is a hypothesis about intent until validated against actual conversions. |
| ACT-6 | Trial-to-Paid Conversion Rate | Trials converting to paid ÷ trials reaching a decision point in the window. | Excluding in-flight trials from the denominator inflates the rate; state the convention. |

## Engagement & Habit

| ID | Metric | Definition | Caution |
|---|---|---|---|
| ENG-1 | Daily Active Users (DAU) | Distinct users performing a defined qualifying action on a given day. | Define the qualifying action precisely; counting every page load makes DAU trivial to inflate. |
| ENG-2 | Weekly Active Users (WAU) | Distinct users performing the qualifying action within a rolling or calendar week. | State rolling vs. calendar week; the two produce different numbers near boundaries. |
| ENG-3 | Monthly Active Users (MAU) | Distinct users performing the qualifying action within a rolling 30 days or calendar month. | Calendar-month and trailing-30-day MAU are not interchangeable; fix one convention. |
| ENG-4 | Stickiness (DAU/MAU) | DAU ÷ MAU for the same window, as a percentage. | Only meaningful for products with an expected daily-use cadence; weekly-cadence tools score low by design. |
| ENG-5 | L28 (Active Days per 28) | Average distinct active days per user across a trailing 28-day window. | Needs the same qualifying-action definition as DAU to stay comparable. |
| ENG-6 | Feature Adoption Rate | Users who used a specific feature at least once ÷ users exposed to or eligible for it. | Separate exposure from eligibility, or a flagged/paywalled feature will read as under-adopted. |

## Retention & Health

| ID | Metric | Definition | Caution |
|---|---|---|---|
| RET-1 | Cohort Retention Rate | Of a cohort starting in period 0, the share still active in period N. | Compare cohorts at equal ages; never a young cohort's early number against an old cohort's mature one. |
| RET-2 | Customer (Logo) Churn Rate | Customers lost in a period ÷ customers at the start of the period. | Treats every account equally regardless of size; pair with revenue churn. |
| RET-3 | Gross Revenue Retention (GRR) | Starting recurring revenue minus downgrades/cancellations ÷ starting recurring revenue, capped at 100%. | Excludes expansion by definition; healthy GRR can still mean flat growth. |
| RET-4 | Net Revenue Retention (NRR) | Starting recurring revenue plus expansion minus downgrades/cancellations ÷ starting recurring revenue. | Excludes new-customer revenue; rising NRR with falling new-logo growth is a different story than broad health. |
| RET-5 | Customer Health Score | A documented, weighted composite of usage, support and billing signals flagging at-risk accounts. | Expose the weights and validate against actual churn; an unvalidated composite is a guess. |
| RET-6 | Repeat Usage Rate | Users/customers with a second qualifying event ÷ those with a first, within a defined window. | A short window undercounts genuine repeat users on a longer natural cycle; check real use cadence first. |

## Monetization & Unit Economics

| ID | Metric | Definition | Caution |
|---|---|---|---|
| MON-1 | Monthly Recurring Revenue (MRR) | Recurring subscription revenue normalized to a monthly figure under the org's stated policy. | Not cash collected; a prepaid multi-year contract still normalizes to a monthly-equivalent rate. |
| MON-2 | Annual Recurring Revenue (ARR) | MRR annualized under the org's normalization policy, typically MRR × 12. | A run rate, not a signed or guaranteed backlog. |
| MON-3 | Average Revenue Per Account (ARPA) | Recurring revenue for the period ÷ number of paying accounts in that period. | State period-average vs. ending account count; they give different denominators. |
| MON-4 | CAC Payback Period | CAC ÷ average monthly gross margin per customer; months to recoup acquisition cost. | Uses gross margin, not revenue, per customer; substituting revenue overstates payback speed. |
| MON-5 | LTV:CAC Ratio | Modeled customer lifetime value ÷ CAC for a comparable cohort. | LTV is modeled and sensitive to the churn assumption behind it; treat a precise ratio from thin data as rough. |
| MON-6 | Rule of 40 | YoY revenue growth rate + profit margin (or FCF margin) — a SaaS efficiency-vs-growth convention, popularized by Brad Feld in 2015, citing a late-stage investor he heard describe it at a board meeting (see [Feld's own post](https://feld.com/archives/2015/02/rule-40-healthy-saas-company/) and [Wikipedia](https://en.wikipedia.org/wiki/Rule_of_40)). | A young company can clear 40 on hypergrowth alone while burning cash; read the two components separately. |
| MON-7 | Magic Number | Net new annualized ARR in a quarter ÷ prior-quarter sales & marketing spend — a common SaaS sales-efficiency signal. | Distorted by one large deal landing at quarter's edge; use a rolling average. |

## Satisfaction & Advocacy

| ID | Metric | Definition | Caution |
|---|---|---|---|
| SAT-1 | Net Promoter Score (NPS) | % promoters (9–10) minus % detractors (0–6) on the standard 0–10 question (Reichheld, *HBR*, 2003). | Denominator includes passives (7–8), excluded from the numerator; attitude, not observed referral behavior. |
| SAT-2 | Customer Satisfaction (CSAT) | Share of respondents choosing "satisfied" on a declared scale, right after a specific interaction. | No universal scale; never merge results from differently worded questions. |
| SAT-3 | Customer Effort Score (CES) | Survey measure of effort required to get a need met (Dixon, Freeman & Toman, *HBR*, 2010). | Scale wording determines whether lower or higher is better; state the wording. |
| SAT-4 | Product/Market Fit Survey Score | Share of users who'd be "very disappointed" if the product disappeared (Sean Ellis's PMF test). | The commonly cited 40% threshold is a rule of thumb from Ellis's own writing, not a validated cutoff. |
| SAT-5 | Referral Coefficient (K-factor) | Invitations sent per user × conversion rate of those invitations, for a defined referral cycle. | A K-factor above 1 implies compounding growth only if both rates hold as the base grows; they typically decay. |

## Delivery Flow

Sourced from the four DORA metrics (Forsgren, Humble & Kim, *Accelerate*, 2018; DORA's public
State of DevOps research) rather than kanban-style flow metrics — a deliberately different lens
on delivery health than throughput/WIP/cycle-time analysis.

| ID | Metric | Definition | Caution |
|---|---|---|---|
| FLOW-1 | Deployment Frequency | How often the team ships to production within a period. | A high count of trivial or reverted deploys isn't the same signal as frequent, safe delivery. |
| FLOW-2 | Lead Time for Changes | Elapsed time from commit to running in production. | State whether queued review/approval time is included, or the figure understates real lead time. |
| FLOW-3 | Change Failure Rate | Share of deployments causing a degradation requiring remediation. | Needs a consistent, agreed definition of "failed change" or trend comparisons are meaningless. |
| FLOW-4 | Time to Restore Service | Elapsed time from incident detection to resolution. | Detection time varies with monitoring coverage; a monitoring gap can make restoration look artificially fast. |

Cohort analysis, funnel analysis and segmentation are complementary *methods*, not additional
entries in this list — each can be applied to most of the metrics above rather than standing
alone as its own row.
