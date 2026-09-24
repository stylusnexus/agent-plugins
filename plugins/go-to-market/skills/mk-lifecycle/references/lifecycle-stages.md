# Lifecycle stages

A lifecycle stage answers one question: how far has this contact actually progressed in their relationship with the product, independent of any single campaign or list they're on. HubSpot's knowledge base defines the property directly: "Use lifecycle stages to categorize your contacts and companies based on where they are in your marketing and sales processes." ([Use contact and company lifecycle stages](https://knowledge.hubspot.com/records/use-lifecycle-stages))

## The stages, in order

HubSpot's default set, as defined on that page:

1. **Subscriber** — "a contact that has opted in to hear more from you by signing up for your blog or newsletter."
2. **Lead** — "a contact or company that has converted on your website or through some other interaction with your organization beyond a subscription sign up."
3. **Marketing Qualified Lead** — "a contact or company that your marketing team has qualified as ready for the sales team."
4. **Sales Qualified Lead** — "a contact or company that your sales team has qualified as a potential customer." HubSpot notes this stage "includes sub-stages that are stored in the Lead Status property" — a separate, more granular field for where sales is in working the contact.
5. **Opportunity** — "a contact or company that is associated with a deal."
6. **Customer** — "a contact or company with at least one closed deal."
7. **Evangelist** — "a customer that has advocated for your organization."
8. **Other** — "a contact or company that does not fit any of the above stages."

Most small teams won't use all eight from day one. A pre-revenue product might only need Subscriber, Lead, and Customer defined until Sales Qualified Lead and Opportunity become real distinctions worth tracking — adopt stages as the process actually needs them, not because the full list exists.

## It only moves forward, by default

HubSpot's own behavior is directional: "default automatic updates to the lifecycle stage property will only move the stage forward" — a workflow or form submission can take a contact from Lead to Customer, never back. Moving a stage backward requires a manual edit to the record. This matters for how a lifecycle map gets built: automation should express "this contact reached stage X," never "this contact might have left stage X," because the property isn't designed to track disengagement on its own — that's a separate signal (a status field, an unsubscribe, a churn flag), not a lifecycle-stage reversal.

## How a stage actually changes

A contact's lifecycle stage can update automatically — through form submissions, list imports, workflows, API calls, or other integrations — or be set manually by editing a single record or bulk-editing from a list view. Whichever path sets it, the property then works like any other: it can be used to filter lists, build workflow automation, and segment contacts for reporting.

## Using this in a lifecycle map

When mapping a product's lifecycle, name the trigger that moves someone into each stage and the trigger for the next one, using only stages the team can actually detect. A stage nobody has a way to observe isn't a stage yet — it's a wish. Keep the automatic-forward-only behavior in mind when deciding what "success" looks like for an email sequence: the sequence's job is to earn the next forward move, not to guess at signals the stage property was never built to represent.
