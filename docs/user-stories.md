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

