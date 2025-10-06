from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    task_duration: str
    assignee_name: Optional[str] = None  # optional


class TaskRead(BaseModel):
    id: int
    title: str
    task_duration: str
    assignee_name: Optional[str] = None  # optional
