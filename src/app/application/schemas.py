from pydantic import BaseModel

from app import domain


class TaskCreate(BaseModel):
    task_id: int
    title: str
    description: str
    status: str
    creator_token: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: domain.TaskStatus

class UserCreate(BaseModel):
    name: int
    admin: int

class UserUpdate(BaseModel):
    name: int
    admin: int