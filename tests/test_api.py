# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db
from app.database import Base  # your declarative_base()

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    # If you need to reset your test DB, do it here.
    # e.g. drop & recreate tables, or use a separate TEST_DATABASE_URL.
    yield


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()


def test_create_list_get_update_delete_task():
    # 1) Create
    payload = {
        "title": "Test Task",
        "description": "pytest flow",
        "due_at": "2025-07-20T12:00:00Z",
        "user_email": "you@example.com"
    }
    r = client.post("/tasks/", json=payload)
    assert r.status_code == 201
    task = r.json()
    tid = task["id"]

    # 2) List
    r = client.get("/tasks/")
    assert r.status_code == 200
    assert any(t["id"] == tid for t in r.json())

    # 3) Get by ID
    r = client.get(f"/tasks/{tid}")
    assert r.status_code == 200
    assert r.json()["title"] == payload["title"]

    # 4) Update
    update = payload.copy()
    update["title"] = "Updated via pytest"
    r = client.put(f"/tasks/{tid}", json=update)
    assert r.status_code == 200
    assert r.json()["title"] == "Updated via pytest"

    # 5) Delete
    r = client.delete(f"/tasks/{tid}")
    assert r.status_code == 204
    assert r.json()["detail"] == "Task deleted"

    # 6) Confirm deletion
    r = client.get(f"/tasks/{tid}")
    assert r.status_code == 404

