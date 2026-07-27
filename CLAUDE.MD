# CLAUDE.md

This file provides guidance for the Module 4 Task Tracker repository.

## Tech stack

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- pytest
- httpx
- Vanilla JavaScript frontend in frontend/index.html

## Run command

```bash
uvicorn app.main:app --reload --port 8000
```

## Test command

```bash
pytest -v
```

## Architecture summary

- Backend: app/main.py defines the FastAPI endpoints for /health, /tasks, /tasks/{task_id}, and /activity.
- Backend: app/models.py defines the Pydantic request/response models, enums, and validation rules.
- Backend: app/storage.py holds the in-memory task store and activity event history.
- Backend: app/business_rules.py contains the task status transition rules.
- Frontend: frontend/index.html is the static UI that calls the API directly.
- Tests: tests/ contains pytest coverage and fixtures; tests/conftest.py resets state between tests.

## Business rules

- Task status values implemented in code: ToDo, InProgress, Done.
- Transition rules implemented in app/business_rules.py:
  - ToDo -> InProgress
  - InProgress -> Done
  - Done -> InProgress
  - Same-status updates are allowed as no-ops
  - ToDo -> Done and any -> ToDo transitions are not allowed

## UI states and CORS notes

- The frontend includes a Kanban-style board with loading skeletons, an empty state, and error cards.
- CORS is configured in app/main.py for http://localhost:5500, http://127.0.0.1:5500, http://localhost:5173, and "null" for file:// usage.

## Do-not rules

- Do not add authentication.
- Do not add a database.
- Do not add deployment steps.
- Do not make major UI changes without asking.

