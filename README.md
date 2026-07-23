# Task Tracker API

A simple task management app with a FastAPI backend and a static frontend.

## Project structure

- `app/` — FastAPI application, business rules, storage, and models
- `frontend/` — static HTML/CSS/JavaScript UI
- `tests/` — pytest-based tests

## Requirements

- Python 3.10+
- pip

## Setup

From the project root, create and activate a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the backend

Start the API server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- http://127.0.0.1:8000/docs for the Swagger UI
- http://127.0.0.1:8000/health for the health check endpoint

## Run tests

```bash
pytest
```
