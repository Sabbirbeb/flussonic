from pydantic import BaseModel

from app import domain


class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    creator_token: str


class TaskUpdate(BaseModel):
    title: str
    description: str
    status: domain.TaskStatus

class UserCreate(BaseModel):
    name: str
    admin: bool

class UserUpdate(BaseModel):
    admin: bool