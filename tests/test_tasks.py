import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.schema import Base
from app.api.tasks import get_task_service
from app.main import app  # your FastAPI app
from app.services.task_service import TaskService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_task_service():
    db = TestingSessionLocal()
    try:
        yield TaskService(db)
    finally:
        db.close()

app.dependency_overrides[get_task_service] = override_get_task_service

client = TestClient(app)


def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}



def test_create_task():
    payload = {"title": "Test Task", "task_duration": "5 days", "assignee_name": "TestUser1"}
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["task_duration"] == "5 days"
    assert data["assignee_name"] == "TestUser1"
    assert "id" in data


def test_list_tasks():
    response = client.get("/api/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # previous test added one task


def test_get_task():
    # First, create a task
    payload = {"title": "Fetch Task", "task_duration": "3 days", "assignee_name": "TestUser2"}
    create_resp = client.post("/api/tasks", json=payload)
    task_id = create_resp.json()["id"]

    # Fetch it
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Fetch Task"
    assert data["assignee_name"] == "TestUser2"


def test_update_task():
    # First, create a task
    payload = {"title": "Old Task", "task_duration": "2 days", "assignee_name": "TestUser3"}
    create_resp = client.post("/api/tasks", json=payload)
    task_id = create_resp.json()["id"]

    # Update it
    update_payload = {"title": "Updated Task", "task_duration": "2 days", "assignee_name": "TestUser4"}
    response = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["assignee_name"] == "TestUser4"


def test_delete_task():
    # Create a task to delete
    payload = {"title": "Delete Me", "task_duration": "1 day", "assignee_name": "TestUser2"}
    create_resp = client.post("/api/tasks", json=payload)
    print(create_resp.content)
    task_id = create_resp.json()["id"]

    # Delete it
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"success": True}

    # Check that it no longer exists
    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 404
