# AI Playbook

## When I reach for AI first
I use AI most often for drafting documentation, reviewing diffs, explaining config errors, and proposing small CI or Docker changes. It is especially helpful when I need a quick first pass on a README section, a workflow snippet, or a debugging hypothesis.

## When I do not reach for AI first
I slow down when a change touches core app behavior, business rules, security-sensitive code, or anything that could expand the product beyond the course scope. I also avoid AI when I do not yet understand the repository enough to judge the suggestion.

## My non-negotiables
- I do not paste secrets, tokens, environment values, or personal data into AI tools.
- I verify AI output by running tests, checking /health, or inspecting the relevant files directly.
- I keep work minimal and explain any change that touches app/ or frontend/.

## My review rules
- I read the diff before accepting anything.
- I verify commands and expected behavior with the actual repo rather than trusting the first suggestion.
- I grade AI comments by usefulness, noise, or wrongness and keep the evidence in docs/.

## What I am still figuring out
I am still learning when AI is strong at scaffolding and when it becomes too eager to over-solve a problem. I want to keep getting better at spotting suggestions that are technically plausible but outside the real goal.

## Decision Card
- New feature: pause and ask whether it fits the scope.
- Code review: compare the suggestion to the repo rules and current behavior.
- Debugging: test the hypothesis before changing code.
- Infrastructure: verify CI and Docker behavior with real commands.
- Never paste: secrets, credentials, or personal data.
- One rule: if I cannot explain a changed line, I do not ship it.
