Feature 1: Search + combined filters

ID: US-01
Story: As a team member, I want to type keywords into a search bar so that I can quickly find tasks by title or description without scanning the whole board.
Acceptance Criteria:
1. Entering a keyword returns all tasks whose title or description contains the term (case-insensitive), across all three status columns.
2. Matching tasks remain in their kanban columns (ToDo, InProgress, Completed); non-matching tasks are hidden.
3. Clearing the search input restores the full board.
Notes: Substring match is sufficient for Module 1; no fuzzy matching or ranking. Search applies to title + description only.

ID: US-02
Story: As a team member, I want to filter tasks by status and priority so that I can focus on the most urgent work in a specific stage.
Acceptance Criteria: 
1. Selecting a status filter (e.g., InProgress) shows only tasks in that status.
2. Selecting a priority filter (e.g., High) in combination with a status filter shows only tasks matching both conditions (AND logic).
3. Active filters are visually indicated and can be removed individually.
Notes: Priority values assumed to be a fixed set (e.g., Low / Medium / High) defined at task creation.

ID: US-03
Story: As a team member, I want to combine text search with filters (assignee, tag, due date) so that I can narrow results precisely, e.g., "all of Alex's high-priority tasks due this week containing 'API'."
Accceptance Criteria:
1. Search text and any combination of filters apply together with AND logic; results update to reflect all active conditions.
2. A due-date filter supports at least "overdue," "due today," and "due this week" ranges, evaluated against the server date.
3. Removing any single filter re-runs the query with the remaining conditions still applied.
Notes: Assignee is a free-text/simple field since there are no user accounts. Tags assumed to be simple string labels on tasks.

REVISED US-03
ID: US-03
Story: As a team member, I want to combine text search with status, priority, and assignee filters so that I can narrow results precisely, e.g., "all of Alex's high-priority tasks in InProgress containing 'API'."
Acceptance Criteria:
1. Search text and any combination of status, priority, and assignee filters apply together with AND logic; results update to reflect all active conditions.
2. Assignee filter is free text but must match exactly (case-insensitive) against the task's assignee field — no partial/fuzzy matching in Module 1.
3. Removing any single filter re-runs the query with the remaining conditions still applied.
Notes: Naming consistency for assignee is the user's responsibility, since there are no user accounts. Tag and due-date filters are out of scope for Module 1.

Feature 2: Activity Log

ID: US-01
Story: As a team member, I want an event to be recorded when a task is updated so that I can track changes made to a task.
Acceptance Criteria:
1. When a task's fields (such as title, description, or due date) are updated, an activity event is recorded with event type "task_updated", the task ID, and a timestamp.
2. The recorded event includes which fields were changed.
3. GET /activity includes "task_updated" events alongside other event types, in the order they occurred.

ID: US-02
Story: As a team member, I want an event to be recorded when a task is deleted so that I can track when tasks are removed.
Acceptance Criteria:
1. When a task is deleted, an activity event is recorded with event type "task_deleted", the task ID, and a timestamp.
2. The event is recorded even though the underlying task no longer exists.
3. GET /activity still returns "task_deleted" events for tasks that have since been removed.


ID: US-03
Story: As a team member, I want GET /activity to return events ordered by most recent first so that I can quickly see the latest changes.
Acceptance Criteria:
1. GET /activity returns events sorted in descending order by timestamp.
2. If two events share the same timestamp, they are returned in the order they were recorded.
3. The response format and fields remain consistent regardless of the number of events returned.
REVISED US-03
Story: As a team member, I want GET /activity to return events ordered by most recent first, with support for retrieving them in manageable pages, so that I can review recent activity without loading the entire history at once.
Acceptance Criteria:
1. GET /activity returns events sorted in descending order by timestamp.
2. GET /activity supports optional pagination parameters (e.g., limit and offset) to control how many events are returned per request.
3. If no pagination parameters are provided, the endpoint returns a reasonable default number of the most recent events rather than the full history.