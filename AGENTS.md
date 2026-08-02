# AGENTS.md

## Project stack
- Python 3.11
- FastAPI
- Pydantic v2
- pytest
- httpx
- Vanilla JavaScript frontend in frontend/index.html

## Run and test commands
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8000
pytest -v
```

## Repo-specific rules
- Keep the work inside the course scope: no authentication, no production database, no notifications, and no unrelated UI rewrites.
- Prefer documentation, CI, Docker, and small bug-fix changes over new product features.
- If a change touches app/ or frontend/, explain the reason in docs/final-ai-review.md and keep the change minimal.
- Never paste secrets, real customer data, or environment values into AI tools.
- Verify AI suggestions by reading the relevant files and running the app, tests, or container checks before accepting them.

## Docs-first and read-first guardrails
- Read the relevant source files and existing docs before editing.
- Update README and docs when behavior changes or when release readiness is being claimed.
- If you cannot explain a changed line, command, or configuration choice, do not submit it as final work.
