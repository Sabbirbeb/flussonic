from pydantic import BaseModel, Field

class SkipLimit(BaseModel):
    skip: int = Field(
        None, ge=1, description="Skip", json_schema_extra={"example": 1}
    )
    limit: int = Field(
        None, ge=1, description="Limit", json_schema_extra={"example": 50}
    )


class CreateTask(BaseModel):
    title: str = Field(
        None, description="Name", json_schema_extra={"example": "Task 1"}
    )
    description: str = Field(
        None,
        description="description",
        json_schema_extra={"example": "Complete the project"},
    )


class UpdateTask(BaseModel):
    title: str = Field(
        None, description="Name", json_schema_extra={"example": "Updated task"}
    )
    description: str = Field(
        None,
        description="description",
        json_schema_extra={"example": "Review the code changes"},
    )


class GetTask(BaseModel):
    task_id: int = Field(
        None, ge=1, description="Tasks ID", json_schema_extra={"example": 1}
    )

class Task(BaseModel):
    task_id: int = Field(
        None, ge=1, description="Tasks ID", json_schema_extra={"example": 1}
    )
    title: str = Field(
        None, description="Name", json_schema_extra={"example": "Updated task"}
    )
    description: str = Field(
        None,
        description="description",
        json_schema_extra={"example": "Review the code changes"},
    )
    user_id: int = Field(
        None,
        description="User id",
    )

class GetUsersResponse(BaseModel):
    class User(BaseModel):
        id: int
        name: str
        admin: bool

    users: list[User]
