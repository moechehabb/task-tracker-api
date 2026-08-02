# Final AI Review and Ownership Evidence

## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| “Add authentication so the app is production-ready.” | Wrong | That would expand the project beyond the course scope and violate the repo rules. | Rejected and kept the work limited to documentation, CI, and release readiness. |
| “Replace the static frontend with a React app.” | Wrong | The current frontend is part of the existing scope and does not need a framework rewrite for this submission. | Kept the existing vanilla JavaScript frontend unchanged. |
| “Add more feature work to the task board.” | Useful | The suggestion was not harmful, but it would have introduced new product surface area rather than helping release readiness. | I downgraded it to documentation and verification work only. |

## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| The container should not bake in local secrets or environment files. | `.dockerignore`, `Dockerfile` | Valid | The repo excludes `.env` files and only copies the application code and requirements. | Keep the current packaging approach. |
| CI should not use skip-style shortcuts for tests. | `.github/workflows/ci.yml` | Valid | The workflow runs the pytest command directly and does not use `continue-on-error` or `|| true`. | Keep the workflow as-is. |
| The frontend’s direct API URL is a potential deployment assumption. | `frontend/index.html` | Noise | It is a runtime assumption, not a security flaw in the current local development setup. | No change needed for this submission. |

## Manual security check
I manually checked the Docker build context, workflow commands, and repo instructions for obvious release risks. I confirmed that the Docker image does not copy `.env` files, the CI workflow runs pytest directly, and the documentation reflects the actual local commands rather than a hypothetical setup.

## One AI output I rejected or corrected
An AI suggestion proposed adding authentication and a larger UI rewrite to make the app feel “more complete.” I rejected that direction because the course rules explicitly forbid new product features and the goal of this submission is release evidence, not feature expansion. I kept the repo aligned to the existing task tracker scope and documented the evidence instead.

## Three AI usage rules
1. Never paste: secrets, `.env` values, tokens, or real customer data into any AI tool.
2. Always verify: run the relevant tests, health checks, or container commands before trusting AI output.
3. Record AI contributions by: saving the relevant review notes, diffs, and decisions in docs/ so the repository shows what was reviewed and why.

## Ownership statement
I am comfortable submitting this repository as my own work because I verified the actual commands, checked the runtime behavior of the API and Docker container, and kept the final changes focused on release readiness, documentation, and evidence. I understand the code paths that were touched and I can explain the decisions in the repository notes. The final deliverables reflect a real, tested submission rather than a blind acceptance of AI-generated text or configuration.
