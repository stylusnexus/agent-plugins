# Product metrics reference

All 55 named measures/analyses in the ProductCompass reference list are indexed below. Definitions are suite operational interpretations, with source simplifications clarified. Select measures for the decision; do not track everything. Every implementation needs event/field definitions, unit, cohort, window, numerator/denominator where relevant, owner, source, freshness, baseline and guardrails. Finance-related definitions require reconciliation with the organization’s reporting policy; this is not accounting advice.

| ID | Area | Metric | Working definition | Caution |
|---|---|---|---|---|
| M01 | Acquisition | Bounce Rate | Share of sessions classified as bounced. | Use the analytics tool’s explicit definition; single-page visits are not universally bounces. |
| M02 | Acquisition | Conversion Rate | Eligible users or visits completing a defined action divided by eligible users or visits. | Specify unit, cohort, attribution and conversion window. |
| M03 | Acquisition | Landing Page Conversion Rate | Eligible landing-page visitors completing the chosen action divided by eligible visitors. | Separate pages and traffic cohorts; define repeat visits. |
| M04 | Acquisition | Customer Acquisition Cost (CAC) | Defined acquisition costs divided by newly acquired customers. | State included costs, timing, customer definition and attribution lag. |
| M05 | Acquisition | Cost Per Acquisition (CPA) | Campaign costs divided by attributed target actions. | An action need not be a paying customer; distinguish from CAC. |
| M06 | Acquisition | Channel Effectiveness | Comparison of channel outcomes against costs and goals. | A family of measures, not one standard formula; compare retained value. |
| M07 | Acquisition | Traffic Source Distribution | Share of eligible traffic attributed to each source. | Define attribution model and unknown/direct traffic. |
| M08 | Acquisition | Cost Per Click (CPC) | Advertising spend divided by attributable clicks. | Cheap clicks do not establish customer value. |
| M09 | Acquisition | Click-Through Rate (CTR) | Clicks divided by impressions for a defined placement. | Specify total or unique counts; check downstream outcomes. |
| M10 | Activation | Time to Value (TTV) | Elapsed time from a defined starting event to a meaningful value event. | Report distribution and users who never reach value, not just successful users. |
| M11 | Activation | Onboarding Completion Rate | Eligible starters completing a defined onboarding flow within a window. | Completion does not necessarily mean achieved value. |
| M12 | Activation | User Activation Rate | Eligible users reaching a defined value-related milestone within a window. | Validate the milestone’s relationship to value and retention. |
| M13 | Activation | Trial-to-Paid Conversion Rate | Eligible trials becoming paid within a defined window. | Account for trials still running and consistent cohort timing. |
| M14 | Activation | First-time User Conversion Rate | First-time users completing a specified action within a window. | Define first-time identity and action. |
| M15 | Activation | Product Qualified Leads (PQL) | Users meeting documented product-usage qualification rules. | A rule-based count or rate, not automatic proof of purchase intent. |
| M16 | Activation | Product Qualified Accounts (PQA) | Accounts meeting documented account-level qualification rules. | Define aggregation across users and account eligibility. |
| M17 | Engagement | Daily Active Users (DAU) | Distinct users performing qualifying activity in a day. | Specify activity, timezone and identity deduplication. |
| M18 | Engagement | Monthly Active Users (MAU) | Distinct users performing qualifying activity in a month. | Calendar month and rolling 30 days are different conventions. |
| M19 | Engagement | Stickiness | A stated DAU-to-MAU ratio. | Define the daily statistic and matching window; not suitable for every usage cadence. |
| M20 | Engagement | User Satisfaction (CSAT) | Survey satisfaction measure using a declared scale and aggregation. | Define satisfied responses and denominator; report response bias. |
| M21 | Engagement | Session Length | Elapsed duration of a defined session. | Inactivity timeout and background activity matter; longer can mean friction. |
| M22 | Engagement | Session Frequency | Sessions per user in a defined window. | Specify eligible population and expected use cadence. |
| M23 | Engagement | Feature Usage | Adoption, frequency or depth of a defined feature interaction. | Separate availability, exposure and successful use; no single standard formula. |
| M24 | Engagement | Customer Effort Score (CES) | Survey measure of perceived effort or ease. | Scale wording determines direction; lower is not universally better. |
| M25 | Engagement | Task Success Rate | Successful eligible attempts divided by eligible task attempts. | Define task, success, partial success and assisted attempts. |
| M26 | Engagement | User Feedback Score | A defined aggregation of user ratings. | No universal scale; do not merge incompatible questions or scales. |
| M27 | Retention | Churn Rate | Share of an eligible starting population lost in a defined period. | Distinguish customer, user-activity and revenue churn; define lost and reactivation. |
| M28 | Retention | User Retention Rate | Share of an eligible starting cohort meeting a return/value criterion. | State exact-day, rolling or bounded-window convention. |
| M29 | Retention | Cohort Retention Analysis | Retention compared across groups with a common starting condition. | An analysis method, not a single number; compare equal cohort ages. |
| M30 | Retention | User Renewal Rate | Eligible contracts or subscriptions renewed divided by those due. | Exclude not-yet-due renewals and define grace periods. |
| M31 | Retention | Customer Lifetime | Duration of a customer relationship under a defined end condition. | Active relationships are censored; observed duration is not completed lifetime. |
| M32 | Retention | Customer Health Score | Documented composite of usage, service and relationship signals. | Expose weights, missingness and validation; not an objective universal score. |
| M33 | Retention | Product Adoption Rate | Eligible users or accounts adopting a product/feature within a window. | Define adoption as meaningful behavior rather than exposure alone. |
| M34 | Revenue | Average Revenue Per Account (ARPA) | Period revenue divided by the consistently defined account base. | State revenue scope, currency, period and average versus ending account count. |
| M35 | Revenue | Customer Lifetime Value (CLV/LTV) | Observed or modeled lifetime revenue or contribution per customer. | Declare revenue versus margin basis, horizon and assumptions; do not infer from thin churn data. |
| M36 | Revenue | Customer Profitability | Customer-attributed revenue less relevant costs under a declared method. | LTV minus CAC and LTV/CAC are different economics measures, not interchangeable profit formulas. |
| M37 | Revenue | Monthly Recurring Revenue (MRR) | Monthly-normalized recurring subscription revenue. | Define discounts, usage components, currency and exclusions; not cash collected. |
| M38 | Revenue | Annual Recurring Revenue (ARR) | Annualized recurring run rate under the chosen policy. | Often 12 times comparable MRR; not guaranteed future revenue or bookings. |
| M39 | Revenue | Expansion Revenue | Added recurring or other defined revenue from existing customers. | Separate upgrades, cross-sells, price changes and new customers. |
| M40 | Revenue | Average Contract Value (ACV) | Average contract value under an explicit annualized or total-value convention. | Do not confuse total contract value with annual value; document one-time charges. |
| M41 | Revenue | Gross Margin | Revenue less cost of revenue; percentage divides that amount by revenue. | Distinguish dollars from percent and follow the applicable cost classification; sales expense is not automatically cost of revenue. |
| M42 | Revenue | Net Revenue Churn | Starting-cohort revenue lost to churn/contraction less expansion, often divided by starting revenue. | Specify reactivation policy; exclude new-customer revenue; can be negative. |
| M43 | Revenue | Net Revenue Retention (NRR) | Starting-cohort recurring revenue retained including expansion/contraction/churn divided by starting recurring revenue. | Exclude new customers; same scope and policies are needed to compare with net revenue churn. |
| M44 | Referral | Virality Coefficient | Attributed new users generated per originating user in a defined referral cycle. | State invitations and conversion assumptions; cycle time and saturation matter. |
| M45 | Referral | Customer Referral Rate | Eligible customers making a qualifying referral divided by eligible customers. | Define completed referral versus merely sharing a link. |
| M46 | Referral | Referral Conversion Rate | Eligible referred prospects becoming qualified active users/customers divided by referred prospects. | Specify conversion event, window and attribution. |
| M47 | Referral | Net Promoter Score (NPS) | For the standard 0–10 question, percent 9–10 responses minus percent 0–6 responses. | Denominator includes valid 7–8 responses; score is attitude, not observed referral behavior. |
| M48 | Flow | Lead Time | Elapsed time from an agreed request/commitment point to the agreed completion point. | Choose explicit boundaries; backlog entry is not universal. |
| M49 | Flow | Time to Market (TTM) | Elapsed time from the chosen idea/opportunity start to customer availability. | Document boundaries and scope; compare equivalent work. |
| M50 | Flow | Cycle Time | Elapsed time from work start to the defined finished state. | State inclusion of waiting and blocked time; use distributions. |
| M51 | Flow | Work In Progress (WIP) | Count of items started and not finished at a point in time. | Use consistent workflow boundaries and item granularity. |
| M52 | Flow | Throughput | Count of finished comparable work items per time unit. | Throughput measures flow, not customer value; do not mix incompatible item sizes blindly. |
| M53 | Flow | Time to Learn (TTL) | Elapsed time from a question/test starting point to decision-relevant evidence. | Define the learning decision; shipping or collecting events alone is not learning. |
| M54 | Flow | Work Item Age | Elapsed time since start for an unfinished item. | Use the same start boundary as cycle time; do not count it as completed cycle time. |
| M55 | Flow | Velocity | Team-estimated work units completed per iteration. | Team-local planning aid; do not compare people/teams or interpret points as value. |

Source: Paweł Huryn, The Ultimate List of Product Metrics, May 27, 2023, updated November 4, 2024. Cohort analysis, funnel analysis and segmentation are complementary methods. Little’s Law relates average WIP, throughput and time only under compatible stable-system assumptions; it is not a guarantee that reducing WIP alone increases throughput.
