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

## View the frontend

The frontend is a static page that calls the backend API.

1. Start the backend as shown above.
2. In a second terminal, serve the frontend files:

```bash
python3 -m http.server 5500 --directory frontend
```

3. Open the UI in your browser:

```text
http://127.0.0.1:5500
```

## Run tests

```bash
python3 -m pytest
```
