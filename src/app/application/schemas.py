from pydantic import BaseModel


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


class User(BaseModel):
    id: int
    name: str
    admin: bool
