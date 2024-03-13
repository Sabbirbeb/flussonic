from pydantic import BaseModel

from app import domain


class TaskCreate(BaseModel):
    title: str
    description: str
    user_id: int


class TaskUpdate(BaseModel):
    title: str
    description: str

class UserCreate(BaseModel):
    name: str
    admin: bool

class UserUpdate(BaseModel):
    admin: bool