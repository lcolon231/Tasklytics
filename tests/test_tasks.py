import pytest
from datetime import datetime, timezone

def test_update_task_success(client):
    # First, create a task
    payload = {
        "title": "To be updated",
        "description": "orig",
        "due_at": datetime.now(timezone.utc).isoformat(),
        "user_email": "u@example.com"
    }
    res = client.post("/tasks/", json=payload)
    task = res.json()
    task_id = task["id"]

    # Now update just the title and description
    update_payload = {
        "title": "Updated!",
        "description": "new desc"
    }
    res = client.put(f"/tasks/{task_id}", json=update_payload)
    assert res.status_code == 200
    updated = res.json()
    assert updated["title"] == "Updated!"
    assert updated["description"] == "new desc"
    # unchanged fields
    assert updated["user_email"] == payload["user_email"]

def test_update_task_not_found(client):
    res = client.put("/tasks/99999", json={"title": "x"})
    assert res.status_code == 404
    assert res.json()["detail"] == "Task not found"

def test_delete_task_success(client):
    # create a task to delete
    payload = {
        "title": "To be deleted",
        "due_at": datetime.now(timezone.utc).isoformat(),
        "user_email": "u2@example.com"
    }
    res = client.post("/tasks/", json=payload)
    task_id = res.json()["id"]

    # delete it
    res = client.delete(f"/tasks/{task_id}")
    assert res.status_code == 204

    # confirm it's gone
    res = client.get(f"/tasks/{task_id}")
    assert res.status_code == 404

def test_delete_task_not_found(client):
    res = client.delete("/tasks/54321")
    assert res.status_code == 404
    assert res.json()["detail"] == "Task not found"
