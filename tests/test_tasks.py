class TestCreateTask:
    def test_create_task_valid_returns_201_with_full_body(self, client):
        response = client.post(
            "/tasks",
            json={
                "title": "Write tests",
                "description": "Cover the API",
                "status": "ToDo",
                "priority": "High",
                "assignee": "moe",
            },
        )
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Write tests"
        assert body["description"] == "Cover the API"
        assert body["status"] == "ToDo"
        assert body["priority"] == "High"
        assert body["assignee"] == "moe"
        assert "id" in body
        assert "created_at" in body
        assert "updated_at" in body

    def test_create_task_missing_title_returns_422(self, client):
        response = client.post("/tasks", json={"description": "no title"})
        assert response.status_code == 422

    def test_create_task_blank_title_returns_422(self, client):
        response = client.post("/tasks", json={"title": "   "})
        assert response.status_code == 422

    def test_create_task_invalid_priority_returns_422(self, client):
        response = client.post(
            "/tasks", json={"title": "Bad priority", "priority": "Urgent"}
        )
        assert response.status_code == 422

    def test_create_task_unknown_field_returns_422(self, client):
        response = client.post(
            "/tasks", json={"title": "Extra field", "unknown": "nope"}
        )
        assert response.status_code == 422


class TestListTasks:
    def test_list_tasks_empty_returns_200_and_empty_list(self, client):
        response = client.get("/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(
        self, client, created_task
    ):
        response = client.get("/tasks", params={"status": "Done"})
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_filter_by_priority_returns_only_matches(self, client):
        client.post("/tasks", json={"title": "Low one", "priority": "Low"})
        high = client.post("/tasks", json={"title": "High one", "priority": "High"})
        assert high.status_code == 201

        response = client.get("/tasks", params={"priority": "High"})
        assert response.status_code == 200
        body = response.json()
        assert len(body) == 1
        assert body[0]["priority"] == "High"
        assert body[0]["title"] == "High one"

    def test_list_tasks_search_matches_title_and_description_case_insensitively(
        self, client
    ):
        client.post(
            "/tasks",
            json={"title": "Write docs", "description": "Need follow-up"},
        )
        client.post(
            "/tasks",
            json={"title": "Ship feature", "description": "Docs are pending"},
        )

        response = client.get("/tasks", params={"q": "docs"})

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2
        assert {task["title"] for task in body} == {"Write docs", "Ship feature"}

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
        assert len(body) == 1
        assert body[0]["title"] == "Match both"

    def test_list_tasks_no_matches_returns_200_and_empty_list(self, client):
        client.post("/tasks", json={"title": "Existing task"})

        response = client.get("/tasks", params={"q": "nothing"})

        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_invalid_filter_value_returns_422(self, client):
        response = client.get("/tasks", params={"status": "Unknown"})

        assert response.status_code == 422


class TestGetTask:
    def test_get_task_by_id_returns_task(self, client, created_task):
        response = client.get(f"/tasks/{created_task['id']}")
        assert response.status_code == 200
        assert response.json() == created_task

    def test_get_task_by_id_not_found_returns_404_with_detail(self, client):
        response = client.get("/tasks/does-not-exist")
        assert response.status_code == 404
        assert "detail" in response.json()


class TestPatchTask:
    def test_patch_partial_update_keeps_other_fields(self, client, created_task):
        response = client.patch(
            f"/tasks/{created_task['id']}", json={"title": "Updated title"}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["title"] == "Updated title"
        assert body["description"] == created_task["description"]
        assert body["status"] == created_task["status"]
        assert body["priority"] == created_task["priority"]
        assert body["assignee"] == created_task["assignee"]
        assert body["id"] == created_task["id"]

    def test_patch_status_only_keeps_existing_description(self, client):
        create_response = client.post(
            "/tasks",
            json={"title": "Task with description", "description": "Keep me"},
        )
        assert create_response.status_code == 201
        task_id = create_response.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})
        assert response.status_code == 200
        assert response.json()["description"] == "Keep me"
        assert response.json()["status"] == "InProgress"

    def test_patch_not_found_returns_404(self, client):
        response = client.patch("/tasks/does-not-exist", json={"title": "x"})
        assert response.status_code == 404

    def test_patch_valid_transition_todo_to_inprogress_returns_200(
        self, client, created_task
    ):
        assert created_task["status"] == "ToDo"
        response = client.patch(
            f"/tasks/{created_task['id']}", json={"status": "InProgress"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "InProgress"

    def test_patch_invalid_transition_todo_to_done_returns_422(
        self, client, created_task
    ):
        assert created_task["status"] == "ToDo"
        response = client.patch(
            f"/tasks/{created_task['id']}", json={"status": "Done"}
        )
        assert response.status_code == 422

    def test_patch_same_status_returns_422(self, client, created_task):
        assert created_task["status"] == "ToDo"
        response = client.patch(
            f"/tasks/{created_task['id']}", json={"status": "ToDo"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "ToDo"


class TestDeleteTask:
    def test_delete_existing_returns_204_no_body(self, client, created_task):
        response = client.delete(f"/tasks/{created_task['id']}")
        assert response.status_code == 204
        assert response.content == b""

        follow_up = client.get(f"/tasks/{created_task['id']}")
        assert follow_up.status_code == 404

    def test_delete_missing_returns_404(self, client):
        response = client.delete("/tasks/does-not-exist")
        assert response.status_code == 404