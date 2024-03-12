from pydantic import BaseModel, Field
from uuid import UUID

class CreateTask(BaseModel):
    title: str = Field(None, description='Name', json_schema_extra={"example": "Task 1"})
    description: str = Field(None, description="description", json_schema_extra={"example": "Complete the project"})

class GetTask(BaseModel):
    task_id: int = Field(None, description="Tasks ID", json_schema_extra={"example": 1})