# Reading reach metrics on social posts

"Reach" isn't one number — each platform tracks a different set of metrics, defined in its own help documentation, and they aren't interchangeable across platforms. This is a snapshot from one research pass; platform docs and metric definitions change. Re-verify against the live help page before relying on any of this for a real decision, per [shared principles](../../marketing-lead/references/principles.md).

## LinkedIn
LinkedIn's help documentation defines several distinct metrics for a post:
- **Impressions**: "The number of times your post was shown on LinkedIn." On mobile this counts a view once content is "at least 50 percent on the screen for 300 milliseconds or more, or when it's clicked." Impressions can count the same person more than once.
- **Unique impressions / members reached**: "The number of distinct members and Pages that saw your post" — this does *not* count repeat displays to the same person, which is the key difference from impressions.
- **Click-through rate (CTR)**: "The number of clicks your post received divided by the number of impressions your post received."
- **Engagement rate**: "The ratio of interactions per impressions on your post," where interactions include clicks, reactions, comments, and shares.
(LinkedIn Help, "Content analytics for your LinkedIn Page" — https://www.linkedin.com/help/lms/answer/a564051)

## YouTube
YouTube's help documentation separates a few metrics that are easy to conflate:
- **Impressions**: how many times a video's thumbnail was shown to viewers — this is a measure of how often the video was surfaced, not how often it was watched.
- **Impressions click-through rate**: "measures how often viewers watched a video after seeing a registered impression on YouTube," calculated from views that came from a counted impression — not every view originates from a thumbnail impression, so dividing total views by impressions won't match YouTube's own reported CTR. YouTube states roughly half of channels see an impressions CTR between 2% and 10%. (YouTube Help, "Impressions & click-through-rate FAQs" — https://support.google.com/youtube/answer/7628154)
- **Unique viewers**: "the estimated number of viewers who came to watch your videos over a given time period" — a person watching on multiple devices, or watching more than once, still counts as one unique viewer, and the estimate includes both signed-in and signed-out traffic. (YouTube Help, "Understand your unique viewers data" — https://support.google.com/youtube/answer/7577916)

## X

X's own developer documentation defines impressions plainly: "Count of times the post appeared on a user's screen. Not unique — the same user viewing twice counts as two impressions." Beyond impressions, X's public post metrics are reposts (not including quote posts), quote posts, likes, replies, and bookmarks — reported as separate counts by X, not blended into one "engagement" figure. (X, "Metrics" — https://docs.x.com/x-api/fundamentals/metrics)

## What this means for reading a post's real reach
None of these numbers alone answers "did this actually travel." Impressions (or thumbnail impressions) say how often a platform surfaced the content, which is partly a function of how large the existing audience already is — a post can rack up impressions purely from a big follower base without going anywhere new. Unique-viewer or unique-impression figures say how many distinct people that reached, which strips out repeat views from the same follower. Click-through rate and engagement rate say what fraction of the people who saw it actually did something. Reading impressions and unique reach together, over a run of posts rather than a single one, gives a more honest picture than either number alone — a single post's numbers are too noisy on their own to draw a conclusion from.
