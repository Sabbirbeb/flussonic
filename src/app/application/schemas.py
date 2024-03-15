from pydantic import BaseModel

from app.domain import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: TaskStatus


class UserCreate(BaseModel):
    name: str
    admin: bool


class UserUpdate(BaseModel):
    admin: bool


class User(BaseModel):
    id: int
    name: str
    admin: bool
