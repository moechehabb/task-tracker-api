Feature 1: Search + Combined filters

Prompt 1:
You are a product owner writing user stories for a small development team. Context: I am building a Task Tracker web application with a Python/FastAPI backend and a simple web frontend. 

Included features:  
    - Implement a combined text search/filter combinations bar with the following specifications: 
    - Implement text search for a kanban-style task tracker with ToDo, InProgress, Completed status options 
    - Implement filter combinations such as status, priority, assignee, or tag/due-date. 

Explicitly out of scope: 
    - authentication 
    - user accounts 
    - multi-tenancy or per-user task lists 
    - real-time updates 
    - mobile app 
    - notifications 
    - production database or deployment in Module 1 

Target user: A solo developer or small team managing work in a single shared task list. 

Task: Generate 3-5 user stories in the format: As a [role], I want [feature] so that [benefit]. 

Constraints: 
- Use "team member" as the main role unless another role is clearly needed. - For each story, include 2-3 acceptance criteria that are specific and testable. 
- Cover happy paths and at least one failure case across the set. 
- Do not add features outside the scope above. Output format: Return a table with columns: ID, Story, Acceptance Criteria, Notes / Assumptions

Notes: The AI returned a set of user stories with clear roles, benefits, and testable acceptance criteria. I accepted the overall structure and scope, then edited one of the user stories to overcome an assumption done by AI.

Prompt 2: (rewritten from "Review my ADR and tell me if it includes the right things.")
Wrote the ADR below myself. Review it for completeness, but do not rewrite it for me. T

Task:
Check whether my ADR includes: - the chosen architecture and storage approach - why I chose it using simplicity, testability, local run/deploy ability, and familiarity - at least two AI assumptions I corrected or rejected - one or two risks I would address if the project grew Constraints: - Do not generate a replacement ADR. - Do not polish the prose for me. - Give only review feedback and minimal suggestions. AI-Assisted Coding - Module 1 Prompt Library Output format: Return a checklist with columns: Requirement, Present / Missing, Suggested minimal edit. My ADR: 

I am creating a Kanban-Style Task Tracker application and would like to implement a search/combined filter bar functionality. I plan to implement a new /filter endpoint that handles this. The implementation should automatically cover combined filtering: substring match is enough for the title/description, and the user can filter by status, priority, and assigned. There shouldn't be any third party libraries for this.

Notes: The AI returned a checklist-style ADR review with mostly correct coverage. I accepted the core feedback, edited a few points to be more explicit about missing requirements, and rejected any suggestion that would rewrite or polish the ADR prose.

Prompt 3:
You are a senior Python backend engineer. UPDATE ONE existing route in my FastAPI app — do not add a new route.

Context files: @app/main.py @app/models.py @app/storage.py

Target: the existing GET /tasks route.

Operation type: This is an UPDATE to the existing route signature and body, not a new endpoint. Show the change as a diff/replacement of the current GET /tasks function only.

Exact specification:
- Route stays: GET /tasks
- Status code: 200 default is fine
- Tags: ["tasks"]
- Add these optional query params to the existing route (keep any that already exist):
  - q: str | None = None  (substring match, case-insensitive, against title and description)
  - status: TaskStatus | None = None
  - priority: TaskPriority | None = None
  - assignee: str | None = None (exact match, case-insensitive)
- All provided filters combine with AND logic
- Filtering logic runs in-process (no new endpoint, no external query builder, no third-party filtering libraries)
- Response model: list[TaskResponse]
- Behavior: return the filtered list from storage (update storage.get_all_tasks or filter in-route — pick whichever requires the smaller diff against the existing code)
- Empty filter result returns 200 with []

Imports to add only if missing:
from app.models import TaskStatus, TaskPriority, TaskResponse
from app import storage

DO NOT:
- DO NOT create a new /filter or /search endpoint
- DO NOT return 404 for an empty list
- DO NOT manually validate enum values; Pydantic/FastAPI handles invalid query values
- DO NOT add try/except around the storage call
- DO NOT modify POST /tasks or any other route
- DO NOT add any third-party libraries

Output only the imports to add (if missing) and the updated GET /tasks route function, in one code block, showing the full replacement function.

Notes: The AI returned a direct replacement for the GET /tasks route with the requested query parameters and filtering behavior. I accepted the implementation approach, edited the result to keep the route change minimal and scoped to the existing endpoint, and rejected any attempt to add a new endpoint or extra validation.

Feature 2: Activity Log

Prompt 1:

Generate user stories for the Module 1 Task Tracker in the same format and quality as this example.

Feature: Activity Log
Description: Create an event record for task create/update/delete/status changes. Add GET /activity

Example:
Story: As a team member, I want an event to be recorded when a task is created so that I can track task creation.
Acceptance Criteria:
- When a task is created, an activity event is recorded with event type "task_created", the task ID, and a timestamp.
- GET /activity returns a list of events, each including event type, task ID, and timestamp.
- If no events exist, GET /activity returns an empty list with HTTP 200 (not an error).
Now generate five more stories in the same format.
Constraints:
- Use "team member" as the user role.
- Do not mention login, authentication, user accounts, admin roles, notifications, mobile, or real-time updates.
- Include at least one failure case across the generated stories.
Output format:
Return each story with Story and Acceptance Criteria headings.

Notes: The AI returned five activity-log user stories in the requested format. I accepted the story structure, edited the acceptance criteria to make the event payload and empty-list behavior more explicit, and rejected any scope creep beyond the activity log feature.

Prompt 2:
You are a senior Python backend engineer. Add storage functions to my existing storage layer.

Context files: @app/storage.py @app/models.py

Add two functions:

1. record_event(event: ActivityEvent) -> None
   - Appends the event to the activity store.
   - If the write fails for any reason, catch the exception internally, log it (use `logging.getLogger(__name__).error(...)`), and return without raising.
   - Callers must never need to wrap this in try/except — it must not propagate exceptions.

2. get_activity(limit: int = 50, offset: int = 0) -> list[ActivityEvent]
   - Returns events sorted descending by timestamp (most recent first).
   - Events with equal timestamps preserve original insertion order as the tiebreak (i.e. sort must be stable and use insertion order, not just timestamp, as the secondary key).
   - Applies offset then limit after sorting.
   - Returns [] if there are no events or offset exceeds available events.

Behavior notes:
- record_event is fail-soft by design (per spec) — a failed write must never crash or block the caller.
- get_activity must not raise on a partially-populated or empty store.

DO NOT:
- DO NOT change the signature or behavior of any existing storage function (get_all_tasks, create_task, update_task, delete_task, etc.).
- DO NOT make record_event raise on failure — this is intentional, not an oversight.
- DO NOT add retry logic.

Output only the imports to add (if any) and the two new functions in one code block.

Notes: The AI returned storage functions for recording and listing events with fail-soft behavior. I accepted the approach, edited details around sorting stability and offset/limit behavior, and rejected any suggestion to change existing storage functions or add retry logic.

Prompt 3:
You are a senior Python backend engineer. Modify ONE existing route in my FastAPI app to record an activity event.

Context files: @app/main.py @app/models.py @app/storage.py

Target: the existing PATCH/PUT task-update route (whichever exists in main.py — do not rename or change its path, method, or response model).

Exact specification:
- After the task update is successfully applied (i.e. after storage.update_task or equivalent succeeds, before the response is returned):
    - Determine which fields were actually changed by comparing the pre-update task state to the fields present in the update request.
    - Call storage.record_event(...) with:
        - event_type="task_updated"
        - task_id=<the task's id>
        - timestamp=datetime.utcnow() (or this codebase's existing timestamp convention if one exists)
        - changed_fields=<list of field names that changed>
    - Do this only if at least one field actually changed; if the update request results in no actual field changes, do not record an event.
- The route's existing response and status code behavior must be unchanged.

DO NOT:
- DO NOT wrap storage.record_event in try/except — it is fail-soft internally by design.
- DO NOT change the route's path, method, request body schema, or response model.
- DO NOT modify GET /tasks, POST /tasks, DELETE /tasks, or any status-change route.
- DO NOT record an event if the update request contains no actual changes.

Output only the modified route function (full function body) in one code block, plus any new imports needed.

Notes: The AI returned a route update that records an activity event after a successful task update. I accepted the event-recording behavior, edited the change to ensure it only fires for actual field changes, and rejected any version that would record on no-op updates or modify other routes.
