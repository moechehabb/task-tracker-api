from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status

from app import storage
from app.business_rules import validate_status_transition
from app.models import ActivityEvent, TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Task Tracker API",
    description="A learning-focused Kanban-style task management REST API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:5173",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    tags=["System"],
)
def health_check() -> HealthResponse:
    """Return the current health status of the API.

    Returns:
        HealthResponse: A response containing the API status and an ISO-8601
            timestamp for the current UTC time.

    Example:
        GET /health
    """
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    q: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    assignee: Optional[str] = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered by search and task attributes.

    Args:
        q: Optional case-insensitive substring to match against the task title
            or description.
        status: Optional task status filter.
        priority: Optional task priority filter.
        assignee: Optional case-insensitive assignee filter.

    Returns:
        list[TaskResponse]: A list of tasks matching the supplied filters.

    Example:
        GET /tasks?q=bug&status=InProgress&priority=High
    """
    tasks = storage.get_all_tasks(status=status, priority=priority)
    if q is not None:
        needle = q.lower()
        tasks = [
            task
            for task in tasks
            if needle in task.title.lower() or needle in task.description.lower()
        ]
    if assignee is not None:
        needle = assignee.lower()
        tasks = [task for task in tasks if task.assignee is not None and task.assignee.lower() == needle]
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its identifier.

    Args:
        task_id: The unique identifier of the task to fetch.

    Returns:
        TaskResponse: The matching task.

    Raises:
        HTTPException: If no task exists for the supplied identifier, a 404
            error is raised.

    Example:
        GET /tasks/{task_id}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: The task creation payload containing the task details.

    Returns:
        TaskResponse: The newly created task including its generated identifier
            and timestamps.

    Example:
        POST /tasks
        {"title": "Draft PR", "description": "Prepare the release notes"}
    """
    task = storage.add_task(payload)
    storage.record_event(
        ActivityEvent(
            event_type="task_created",
            task_id=task.id,
            timestamp=datetime.now(timezone.utc),
        )
    )
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Update an existing task.

    Args:
        task_id: The unique identifier of the task to update.
        payload: The fields to change on the task.

    Returns:
        TaskResponse: The updated task.

    Raises:
        HTTPException: If the task does not exist, or if the supplied status
            transition is invalid.

    Example:
        PATCH /tasks/{task_id}
        {"status": "Done"}
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)
    existing = storage.get_task_by_id(task_id)
    if existing is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

    updates = payload.model_dump(exclude_unset=True)
    changed_fields = [field for field in updates if getattr(existing, field) != updates[field]]
    if changed_fields:
        storage.record_event(
            ActivityEvent(
                event_type="task_updated",
                task_id=task.id,
                timestamp=datetime.now(timezone.utc),
                changed_fields=changed_fields,
            )
        )
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task by identifier.

    Args:
        task_id: The unique identifier of the task to delete.

    Returns:
        None: A 204 response is returned on success.

    Raises:
        HTTPException: If no task exists for the supplied identifier, a 404
            error is raised.

    Example:
        DELETE /tasks/{task_id}
    """
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    storage.record_event(
        ActivityEvent(
            event_type="task_deleted",
            task_id=task_id,
            timestamp=datetime.now(timezone.utc),
        )
    )


@app.get("/activity", response_model=list[ActivityEvent], tags=["activity"])
def list_activity(limit: int = 5, offset: int = 0) -> list[ActivityEvent]:
    return storage.get_activity(limit=limit, offset=offset)