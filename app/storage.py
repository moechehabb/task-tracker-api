import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from app.models import ActivityEvent, TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_logger = logging.getLogger(__name__)

_tasks: dict[str, TaskResponse] = {}
_events: list[ActivityEvent] = []


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task in memory.

    Args:
        payload: The task creation payload used to build the new task.

    Returns:
        TaskResponse: The created task with a generated identifier and timestamps.
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid.uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
) -> list[TaskResponse]:
    """Return all stored tasks, optionally filtered by status or priority.

    Args:
        status: Optional status filter applied to the task list.
        priority: Optional priority filter applied to the task list.

    Returns:
        list[TaskResponse]: The matching tasks.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Fetch a stored task by identifier.

    Args:
        task_id: The unique identifier of the task to fetch.

    Returns:
        Optional[TaskResponse]: The matching task, if one exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Update a stored task in place.

    Args:
        task_id: The unique identifier of the task to update.
        payload: The task fields to apply to the stored task.

    Returns:
        Optional[TaskResponse]: The updated task, or None if no task exists for
            the supplied identifier.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    if "description" in updates and updates["description"] is None:
        updates["description"] = ""

    updated = task.model_copy(
        update={
            **updates,
            "updated_at": datetime.now(timezone.utc),
        }
    )
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    """Remove a stored task by identifier.

    Args:
        task_id: The unique identifier of the task to delete.

    Returns:
        bool: True if a task was removed, otherwise False.
    """
    if task_id in _tasks:
        del _tasks[task_id]
        return True
    return False


def record_event(event: ActivityEvent) -> None:
    """Record an activity event for later retrieval.

    Args:
        event: The activity event to append to the in-memory event history.

    Returns:
        None.
    """
    try:
        _events.append(event)
    except Exception as exc:
        _logger.error("failed to record activity event: %s", exc)


def get_activity(limit: int = 5, offset: int = 0) -> list[ActivityEvent]:
    """Return a paginated slice of recorded activity events.

    Args:
        limit: The maximum number of events to return.
        offset: The number of events to skip before collecting results.

    Returns:
        list[ActivityEvent]: The requested activity events ordered from newest
            to oldest.
    """
    events = sorted(_events, key=lambda item: item.timestamp, reverse=True)
    return events[offset : offset + limit]


def _reset() -> None:
    _tasks.clear()
    _events.clear()
