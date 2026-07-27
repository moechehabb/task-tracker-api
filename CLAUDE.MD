# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Setup (from project root)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the API server (http://127.0.0.1:8000, Swagger UI at /docs)
uvicorn app.main:app --reload

# Serve the static frontend (in a second terminal, then open http://127.0.0.1:5500)
python3 -m http.server 5500 --directory frontend

# Run all tests
python3 -m pytest

# Run a single test file / single test
python3 -m pytest tests/test_tasks.py
python3 -m pytest tests/test_tasks.py::test_name
```

## Architecture

FastAPI backend with in-memory storage and a static single-file frontend. No database — all state lives in module-level dicts/lists and is lost on restart.

- `app/main.py` — all HTTP endpoints (`/health`, `/tasks` CRUD, `/activity`). Endpoints record `ActivityEvent`s on create/update/delete; updates only record an event when fields actually changed. CORS is configured for the frontend origins (ports 5500 and 5173, plus `"null"` for `file://`).
- `app/models.py` — Pydantic models. All models use `extra="forbid"`. Enum values are CamelCase strings (`ToDo`, `InProgress`, `Done`; `Low`, `Medium`, `High`). Title validation (non-blank, ≤200 chars, stripped) is duplicated in `TaskCreate` and `TaskUpdate`.
- `app/business_rules.py` — status-transition rules. `VALID_TRANSITIONS` defines the allowed Kanban flow (ToDo→InProgress→Done, Done→InProgress, plus same-status no-ops); invalid transitions raise HTTP 422. Note `ToDo→Done` and any →ToDo transitions are disallowed.
- `app/storage.py` — in-memory store keyed by UUID string. `_reset()` clears all state and is used by tests.
- `frontend/index.html` — self-contained static UI that calls the API directly.

## Testing

`tests/conftest.py` provides a `client` fixture (FastAPI `TestClient`), a `created_task` fixture, and an autouse fixture that resets storage before and after every test — tests never share state.

