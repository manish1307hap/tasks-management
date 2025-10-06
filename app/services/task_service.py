from sqlalchemy.orm import Session
from app.db.schema import Task
from sqlalchemy.exc import SQLAlchemyError

class TaskService:
    def __init__(self, session: Session):
        self._db = session

    def list_tasks(self) -> list[Task]:
        return self._db.query(Task).all()

    def get_task(self, task_id: int) -> Task | None:
        return self._db.query(Task).filter(Task.id == task_id).first()

    def create_task(self, title: str, task_duration: str, assignee_name: str | None = None) -> Task:
        task = Task(title=title, task_duration=task_duration, assignee_name=assignee_name)
        try:
            self._db.add(task)
            self._db.commit()
            self._db.refresh(task)
            return task
        except SQLAlchemyError as e:
            print(e)
            self._db.rollback()
            return None

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        assignee_name: str | None = None
    ) -> Task | None:
        task = self.get_task(task_id)
        if not task:
            return None
        if title is not None:
            task.title = title
        if assignee_name is not None:
            task.assignee_name = assignee_name
        try:
            self._db.commit()
            self._db.refresh(task)
            return task
        except SQLAlchemyError:
            self._db.rollback()
            return None

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task(task_id)
        if not task:
            return False
        try:
            self._db.delete(task)
            self._db.commit()
            return True
        except SQLAlchemyError:
            self._db.rollback()
            return False
