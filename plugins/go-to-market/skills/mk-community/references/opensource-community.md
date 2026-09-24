# Open-source and developer community

For an open-source project, the repository is the storefront, manual, and community space at once — most marketing effort belongs in the project itself, not in promotion bolted on afterward. Label each recommendation below as EVIDENCE, INFERENCE, or ASSUMPTION when applying it to a real project.

## Call it "open source" only if it actually is
The Open Source Initiative's Open Source Definition sets ten criteria a license must meet, including free redistribution, included source code, allowed derived works, and no discrimination against persons, groups, or fields of endeavor ([opensource.org/osd](https://opensource.org/osd)). Use the term only if the license clears all ten; otherwise describe the license plainly. A "source available" or partially-restricted license doesn't qualify, and calling it "open source" for reach is a false claim under this suite's honest-persuasion rule.

## The README is the landing page
GitHub's Open Source Guides say a README should answer what the project does, why it's useful, how to get started, and where to get help ([opensource.guide/starting-a-project](https://opensource.guide/starting-a-project/)). People come as users, and later become contributors, "because your project solves a problem for them" ([opensource.guide/finding-users](https://opensource.guide/finding-users/)). INFERENCE: the README's opening lines carry the positioning — write them after the positioning work in `mk-positioning`, not before.

## Docs and the issue tracker are the community surface
- **Say how to join.** A CONTRIBUTING file covers reporting a bug, suggesting a feature, and setting up the environment ([opensource.guide/starting-a-project](https://opensource.guide/starting-a-project/)).
- **Set expectations.** A code of conduct says who the rules apply to and what happens after a violation; the guide points to the Contributor Covenant as a common starting point (same source).
- **Make first steps small.** Label issues simple enough for a newcomer ([opensource.guide/building-community](https://opensource.guide/building-community/)).
- **Answer fast, even when you can't act.** An issue unanswered for a month has probably been forgotten; contributors whose code was reviewed within 48 hours came back far more often (same source). A reply can be a thank-you and a review date.

## Release posture and governance
Treating a release like a product launch, not just a code drop, is the TODO Group's framing: "launching a new OSS project is comparable to a product introduction," needing planning and a maintenance commitment before the first public commit (TODO Group, "A Guide to Outbound Open Source Software" — https://todogroup.org/resources/guides/a-guide-to-outbound-open-source-software/). Its companion guide defines governance as "the process by which the project makes decisions regarding strategy, releases, direction, and development priorities," and advises settling trademark strategy before open-sourcing into a foundation ([todogroup.org/starting-an-open-source-project](https://todogroup.org/resources/guides/starting-an-open-source-project/)).

## Metrics: health over applause
Stars show people noticing, not usage; downloads don't necessarily mean installs or use — referrer data is the more useful signal for whether promotion actually worked ([opensource.guide/metrics](https://opensource.guide/metrics/)). CHAOSS (Community Health Analytics in Open Source Software, a Linux Foundation project) publishes a Starter Project Health model with four metrics: Time to First Response, Change Request Closure Ratio, Contributor Absence Factor, and Release Frequency ([chaoss.community, Starter Project Health](https://www.chaoss.community/kb/metrics-model-starter-project-health/)). The TODO Group adds: set goals before picking metrics, since a healthy niche project may never collect many stars, and not every goal needs a number ([todogroup.org, measuring success](https://todogroup.org/resources/guides/measuring-your-open-source-programs-success/)).

## What this looks like in real, small projects
These aren't composites — each is a named project doing one piece of the pattern above, all drawn from GitHub's own Open Source Guides:
- **Kops** (a Kubernetes project) set aside dedicated, recurring time every other week specifically to help newcomers and work through their pull requests, rather than treating onboarding as something that happens whenever a maintainer has a spare minute ([opensource.guide/building-community](https://opensource.guide/building-community/)).
- **Cookiecutter**'s maintainer grew the contributor base by inviting people to submit a pull request instead of fixing reported issues himself first ([opensource.guide/building-community](https://opensource.guide/building-community/)).
- **Django** built a dedicated landing page to welcome and orient new contributors, and its co-creator called making the project's own website "by far the best thing we did with Django in the early days" ([opensource.guide/building-community](https://opensource.guide/building-community/); [opensource.guide/finding-users](https://opensource.guide/finding-users/)).
- **Rust** publishes a recurring "This Week in Rust" post that names and credits contributors publicly, rather than crediting only in a commit log nobody outside the project reads ([opensource.guide/building-community](https://opensource.guide/building-community/)).

None of these required a launch campaign — each is ordinary maintenance work (a welcome page, a standing time block, a public credit) that doubles as the project's own marketing.
