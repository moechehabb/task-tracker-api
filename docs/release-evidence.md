# Release Evidence

## Baseline
- Branch: final-project
- Date: 2026-08-02
- Local app run command: `uvicorn app.main:app --host 127.0.0.1 --port 8000`
- /health result: `{"status":"ok","timestamp":...}` with HTTP 200
- Frontend check: Served the static UI from `frontend/` on port 5500 and confirmed the page contains the Task Board UI and New Task / Activity Log controls.
- Test command: `python -m pytest -v`
- Test result: Passed after installing dependencies in the local virtual environment.

## CI evidence
- Workflow file: `.github/workflows/ci.yml`
- Latest run link or note: No GitHub Actions run link was available from this environment; the workflow is configured to run `python -m pytest -v` on push and pull request, and the equivalent local test command completed successfully.
- Test command used by CI: `python -m pytest -v`
- Shortcut check: no continue-on-error / no `|| true` / pytest is not skipped.

## Docker evidence
- Build command: `docker build -t task-tracker-api .`
- Run command: `docker run --rm -p 8000:8000 task-tracker-api`
- /health check: Verified locally with `curl http://127.0.0.1:8000/health` returning HTTP 200.
- Non-root check, if implemented: The Dockerfile creates a dedicated `app` user and switches to it before runtime.
- No-baked-secrets check: The container copies only the application code and Python requirements; no `.env` files or secrets are copied into the image.

## Documentation claim-vs-reality log
| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The backend exposes /health and returns HTTP 200. | Local `curl http://127.0.0.1:8000/health` | Pass | No code change needed. |
| The repo can be run locally with a virtual environment and `uvicorn`. | README and local server run | Pass | README was updated with exact commands and a final-project section. |
| The Docker image can build and serve the API on port 8000. | `docker build` and `docker run` plus `/health` check | Pass | Docker instructions were documented in README. |
| CI runs pytest on push and pull request. | `.github/workflows/ci.yml` | Pass | The workflow was aligned to `python -m pytest -v`. |
