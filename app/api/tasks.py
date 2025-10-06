from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.consts.tasks import TasksErrorMessage
from app.db.schema import SessionLocal
from app.models.tasks import TaskCreate, TaskRead
from app.services.task_service import TaskService

router = APIRouter()


def get_task_service() -> TaskService:
    db: Session = SessionLocal()
    try:
        yield TaskService(db)
    finally:
        db.close()


# Health check endpoint
@router.get("/health")
def health_check():
    return {"message": "Hello, FastAPI!"}



# Get all tasks
@router.get("/tasks", response_model=list[TaskRead])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


# Create a new task
@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    created = service.create_task(task.title, task.task_duration, task.assignee_name)
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return created


# Get a single task by ID
@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=TasksErrorMessage.ERROR_TASK_NOT_FOUND)
    return task


# Update a task
@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, task: TaskCreate, service: TaskService = Depends(get_task_service)
):
    updated = service.update_task(
        task_id,
        title=task.title,
        assignee_name=task.assignee_name
    )
    if not updated:
        raise HTTPException(status_code=404, detail=TasksErrorMessage.ERROR_TASK_NOT_FOUND)
    return updated


# Delete a task
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail=TasksErrorMessage.ERROR_TASK_NOT_FOUND)
    return {"success": True}
