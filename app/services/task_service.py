from sqlalchemy.orm import Session

from app.db.schema import Task


class TaskService:
    def __init__(self, session: Session):
        self._db = session

    def list_tasks(self) -> list[Task]:
        return self._db.query(Task).all()

    def get_task(self, task_id: int) -> Task | None:
        return self._db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, title: str, task_duration: str, assignee_name) -> Task:
        task = Task(title=title, task_duration=task_duration, assignee_name=assignee_name)
        self._db.add(task)
        self._db.commit()
        self._db.refresh(task)
        return task

    def update_task(self, task_id: int, name: str) -> Task | None:
        task = self.get_task(task_id)
        if not task:
            return None
        task.name = name
        self._db.commit()
        self._db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        self._db.delete(task)
        self._db.commit()
        return True
