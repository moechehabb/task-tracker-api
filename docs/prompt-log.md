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

Prompt 2:
Wrote the ADR below myself. Review it for completeness, but do not rewrite it for me. T

Task:
Check whether my ADR includes: - the chosen architecture and storage approach - why I chose it using simplicity, testability, local run/deploy ability, and familiarity - at least two AI assumptions I corrected or rejected - one or two risks I would address if the project grew Constraints: - Do not generate a replacement ADR. - Do not polish the prose for me. - Give only review feedback and minimal suggestions. AI-Assisted Coding - Module 1 Prompt Library Output format: Return a checklist with columns: Requirement, Present / Missing, Suggested minimal edit. My ADR: 

I am creating a Kanban-Style Task Tracker application and would like to implement a search/combined filter bar functionality. I plan to implement a new /filter endpoint that handles this. The implementation should automatically cover combined filtering: substring match is enough for the title/description, and the user can filter by status, priority, and assigned. There shouldn't be any third party libraries for this.


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