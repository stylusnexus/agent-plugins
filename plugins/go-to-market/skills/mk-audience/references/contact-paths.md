# What happens to a contact after they sign up

A new signup, subscriber, or lead doesn't stay in one state — they move toward becoming a customer, stall somewhere along the way, or leave. Naming the states explicitly (even without a CRM) is what lets a waitlist or signup flow actually be managed rather than just watched.

## A real, public model of the states

HubSpot's own product documentation defines eight default "lifecycle stages" a contact or company can occupy, in order: **Subscriber** ("opted in to hear more... by signing up for your blog or newsletter"), **Lead** ("converted on your website or through some other interaction... beyond a subscription sign up"), **Marketing Qualified Lead** ("qualified as ready for the sales team"), **Sales Qualified Lead** ("qualified... as a potential customer"), **Opportunity** ("associated with a deal"), **Customer** ("at least one closed deal"), **Evangelist** ("a customer that has advocated for your organization"), and **Other** (doesn't fit the rest). Contacts normally move forward through these; moving backward takes a deliberate action, not an automatic one. Source: HubSpot Knowledge Base, "Use lifecycle stages" — https://knowledge.hubspot.com/contacts/use-lifecycle-stages

This is one vendor's naming, not a universal law — the point worth taking regardless of what a project calls its own stages: a contact needs a small number of named states, movement between them should be an explicit, loggable event, and "hasn't moved in a while" is itself a state worth tracking, not silence.

## When a contact stalls or leaves

CRM practice treats a deal that stops moving as its own tracked state rather than letting it quietly vanish from view: a "closed-lost" opportunity, logged with a reason (lost to a competitor, budget, timing, poor fit) so the pattern across many losses is visible later, not just the single case. Source: aggregated CRM pipeline-stage documentation — https://saleshive.com/glossary/closed-lost ; https://help.close.com/docs/opportunity-statuses

## When a contact comes back

Customer-engagement platforms build explicit workflows for exactly this: identifying a contact who's gone quiet and re-engaging them deliberately, rather than assuming dormant means gone for good. Intercom's own help documentation walks through building a check-in message, a wait step, and a follow-up for a conversation that's gone unresponsive, so re-engagement is a deliberate configured step rather than something that only happens if someone happens to remember. Source: Intercom Help Center, "How to set up an auto follow-up for unresponsive customers" — https://www.intercom.com/help/en/articles/11793341-how-to-set-up-an-auto-follow-up-for-unresponsive-customers

## Applying this without a CRM

A waitlist or signup flow with no dedicated CRM still needs the same logic: name the state a new contact starts in, name what has to happen for them to move to the next state, name what counts as stalled (a time window with no action is a reasonable default), and name what happens when a stalled contact takes action again — they re-enter the flow rather than starting over as if new, since a returning contact isn't the same as a stranger. Keep this simple for a small team: a spreadsheet with a status column, updated honestly, does the job a full CRM does for this purpose.
