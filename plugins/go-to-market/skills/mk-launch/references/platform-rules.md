# Launch platform rules (Show HN, Product Hunt, Reddit)

These notes are a snapshot from one research pass. Platform self-promotion rules change without notice — **re-fetch the live page before relying on any of this for a real launch.**

## Show HN
- The thing being shown has to be usable by a stranger today: real, running software or a working demo, not a landing page, a waitlist, a blog post, or a newsletter behind a signup wall. Those belong in a regular submission, not a Show HN post. (Source: Hacker News, "Show HN" guidelines — https://news.ycombinator.com/showhn.html.)
- It has to be something the poster actually built, and non-trivial — a patch release usually doesn't clear the bar, a real build or overhaul does.
- Never ask for upvotes or comments in the post or the thread. This is explicitly against the rules and the fastest way to get flagged.
- The comment section rewards specificity and curiosity, not a defended pitch — show up ready to answer real technical questions.

## Product Hunt
- Tagline: max 60 characters, "no gimmicks or over-the-top language." Thumbnail: square, 240x240 recommended, under 3MB. An animated GIF is allowed, but "GIFs do not autoplay (they animate on hover)," so the first frame needs to represent the product on its own — and fewer than a third of Product of the Day winners actually used one. Gallery: at least 2 images required, 1270x760. A video is optional but correlated with results: about 53% of products that reached Product of the Day since 2021 included one, and only YouTube links are accepted. (Source: Product Hunt, "Prepare for your launch" — https://www.producthunt.com/launch/preparing-for-launch.)
- The maker's own first comment on the launch is the highest-leverage single asset — 70% of products that hit Product of the Day, Week, or Month had one — and it should introduce the product and who it's for, and ask for feedback, never for upvotes. (Same source as above.)
- Product Hunt's own guidance is that "the best time to launch your product is when you're ready to do so" — but for a launch with no other constraint, it recommends scheduling for 12:01am Pacific to get the full 24-hour homepage cycle, and lets you schedule up to a month ahead. (Same source as above.)
- Whether a brand-new account's votes get down-weighted by the platform is not something Product Hunt states publicly; treat it as unconfirmed, but there's no reason to burn a first-ever account on a first launch regardless.

## Reddit
- Reddit does not currently publish one platform-wide numeric self-promotion ratio. What actually governs a post is that specific subreddit's own rules, posted in its sidebar or wiki — some ban self-promotion outright, some confine it to a weekly thread, some welcome it if the poster participates like a regular member first. The subreddit's own rule always wins over any general assumption about Reddit.
- Read a subreddit's current rules and its recent top posts before posting every time — don't reuse a read from a previous launch without checking again.
- The single most common way to get flagged as spam is posting the same link across many subreddits at once. Pick one community, engage first, and post there before moving to the next.

## Dev-tool launches: the README is the landing page
- GitHub's own guidance for a README is to state what the project does, why it matters, how to get started, and where to get help or contribute — kept short, with anything longer living elsewhere. (Source: GitHub Docs, "About READMEs" — https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes.)
- The first two lines should answer "what is this and why should I care," and a copy-pasteable quickstart beats prose — this is practitioner consensus, not GitHub's own stated guidance, which only says to cover what the project does, why it matters, how to get started, and where to get help.
- Star count alone is a weak read on real adoption: a 2024 academic study of GitHub's fake-star ecosystem found purchased stars "only have a promotion effect in the short term (i.e., less than two months) and become a liability in the long term" once discovered — the count stays inflated even after the interest behind it is gone. (Source: He et al., "Six Million (Suspected) Fake Stars on GitHub: A Growing Spiral of Popularity Contests, Spam, and Malware" — https://arxiv.org/html/2412.13459v2.) Downloads and real issue activity are harder to fake and worth checking alongside stars for that reason, not instead of them.
