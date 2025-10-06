from fastapi import APIRouter, Depends, HTTPException

from app.db.schema import SessionLocal
from app.models.tasks import TaskCreate, TaskRead
from app.services.task_service import TaskService
from app.consts.tasks import TasksErrorMessage
router = APIRouter()


def get_task_service() -> TaskService:
    return TaskService(session=SessionLocal())


@router.get("")
def health_check():
    return {"success": False}


@router.get("/tasks", response_model=list[TaskRead])
def get_tasks(service: TaskService = Depends(get_task_service)):
    return service.list_tasks()


@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)):
    return service.create_task(task.name)


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=TasksErrorMessage.ERROR_USER_NOT_FOUND)
    return task


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, task: TaskCreate, service: TaskService = Depends(get_task_service)
):
    updated = service.update_task(task_id, task.name)
    if not updated:
        raise HTTPException(status_code=404, detail=TasksErrorMessage.ERROR_USER_NOT_FOUND)
    return updated


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail=TasksErrorMessage.ERROR_USER_NOT_FOUND)
    return {"success": True}
