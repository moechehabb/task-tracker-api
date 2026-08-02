# Task Tracker API

A simple task management app with a FastAPI backend and a static frontend.

## Final Project

Branch reviewed: final-project

### What this submission demonstrates
- The existing Task Tracker app still runs inside the intended course scope.
- CI runs the pytest suite on push and pull request.
- The Docker image builds and runs with /health returning 200.
- AI review, security, and ownership evidence is collected in docs/.

### How to run locally

From the project root, create and activate a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the API server:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at:

- http://127.0.0.1:8000/docs for the Swagger UI
- http://127.0.0.1:8000/health for the health check endpoint

Serve the frontend in a second terminal:

```bash
python3 -m http.server 5500 --directory frontend
```

Open the UI in your browser at http://127.0.0.1:5500.

### How to run tests

```bash
pytest -v
```

### How to run with Docker

```bash
docker build -t task-tracker-api .
docker run --rm -p 8000:8000 task-tracker-api
curl http://127.0.0.1:8000/health
```

### Evidence files
- docs/release-evidence.md
- docs/final-ai-review.md
- docs/ai-playbook.md

### AI assistance summary

AI helped draft or review: CI, Docker, docs, and debugging.
I verified the work by: running pytest, reviewing diffs, starting the API, checking /health, and validating the Docker container.
One AI suggestion I rejected or corrected: I rejected a proposal to expand the app beyond the course scope and kept the work limited to documentation, CI, and release readiness.

## Project structure

- app/ — FastAPI application, business rules, storage, and models
- frontend/ — static HTML/CSS/JavaScript UI
- tests/ — pytest-based tests
- docs/ — release evidence and AI review notes

## Requirements

- Python 3.11+
- pip
- Docker (optional for container verification)
