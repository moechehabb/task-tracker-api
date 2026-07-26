# Verification

## Baseline check
- Initial backend test suite was run before implementing the Feature 1 filter/search work.
- The project was expected to support the existing task CRUD behavior while adding query-filter support for GET /tasks.

## Backend test results
The following pytest checks were added and verified for Feature 1:

- Search matches title and description case-insensitively
- Combined status + priority filters use AND logic
- No-match queries return 200 with []
- Invalid filter values return 422

python3 -m pytest -q tests/test_tasks.py -k "search_matches_title_and_description_case_insensitively or combines_status_and_priority_filters_with_and_logic or no_matches_returns_200_and_empty_list or invalid_filter_value_returns_422"

4 passed, 18 deselected in 0.02s

### Command run
```bash
python3 -m pytest -q tests/test_tasks.py
```

### Result
- The relevant Feature 1 tests passed after the implementation was restored and verified.

## Break Test evidence
A break test was performed by introducing a temporary regression in the GET /tasks filter path so one important Feature 1 behavior would fail intentionally.


=================================== FAILURES ===================================
_ TestListTasks.test_list_tasks_combines_status_and_priority_filters_with_and_logic _

self = <test_tasks.TestListTasks object at 0x107719040>
client = <starlette.testclient.TestClient object at 0x1076d6250>

    def test_list_tasks_combines_status_and_priority_filters_with_and_logic(self, client):
        client.post(
            "/tasks",
            json={"title": "Match both", "status": "InProgress", "priority": "High"},
        )
        client.post(
            "/tasks",
            json={"title": "Wrong status", "status": "ToDo", "priority": "High"},
        )
        client.post(
            "/tasks",
            json={"title": "Wrong priority", "status": "InProgress", "priority": "Low"},
        )
    
        response = client.get(
            "/tasks",
            params={"status": "InProgress", "priority": "High"},
        )
    
        assert response.status_code == 200
        body = response.json()
>       assert len(body) == 1
E       AssertionError: assert 3 == 1
E        +  where 3 = len([{'assignee': None, 'created_at': '2026-07-23T10:51:59.459615Z', 'description': '', 'id': 'a6e2c1cd-c9b0-45f5-9335-cd6...ne, 'created_at': '2026-07-23T10:51:59.462386Z', 'description': '', 'id': 'bf26a6bf-d8b8-408d-8e6b-99b4372933da', ...}])

tests/test_tasks.py:110: AssertionError
=========================== short test summary info ============================
FAILED tests/test_tasks.py::TestListTasks::test_list_tasks_combines_status_and_priority_filters_with_and_logic - AssertionError: assert 3 == 1
1 failed, 21 deselected in 0.05s

### Command run
```bash
python3 -m pytest -q tests/test_tasks.py -k "combines_status_and_priority"
```

### Observed failure
- The test failed with an assertion error because the API returned all tasks instead of only the items matching both status and priority.
- This confirmed that the combined-filter logic was not behaving correctly under the broken condition.

### Console log evidence
```text
$ python3 -m pytest -q tests/test_tasks.py -k "search_matches_title_and_description_case_insensitively or combines_status_and_priority_filters_with_and_logic or no_matches_returns_200_and_empty_list or invalid_filter_value_returns_422"
....                                                                     [100%]
4 passed, 18 deselected in 0.02s
```

## Manual browser checks
- The frontend board renders the task columns and supports the new filter/search controls above the board.
- The filter bar updates the visible board results without breaking the existing drag-and-drop interactions.
- The modal flow remains available for creating and editing tasks.
