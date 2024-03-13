from dependency_injector.wiring import inject, Provide
from flask import request
from flask_openapi3 import APIBlueprint, Tag

from functools import wraps

from app import domain
from app.application.service import TaskService
from app.application.schemas import UserCreate
from app.dependencies import get_tasks_service
from app.infrastructure.uow import UnitOfWork
from app.transport.schemas import CreateTask, GetTask, UpdateTask

health_tag = Tag(name="health", description="Health")
health = APIBlueprint(
    "/health", import_name=__name__, url_prefix="/health", abp_tags=[health_tag]
)

tasks_tag = Tag(name="tasks", description="Tasks")
tasks = APIBlueprint(
    "/tasks", import_name=__name__, url_prefix="/tasks", abp_tags=[tasks_tag]
)

user_tag = Tag(name="user", description="User")
user = APIBlueprint(
    "/user", import_name=__name__, url_prefix="/user", abp_tags=[user_tag]
)

security = [
    {"jwt": []},
]


def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        current_user = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        try:
            uow = UnitOfWork()
            async with uow:
                current_user= await uow.users.get_by_name(token)
                if not current_user:
                    current_user = await uow.users.create(UserCreate(name=token,
                                                                     admin=False))
                    await uow.commit()
            print (current_user.name)
            if not current_user:
                return {
                    "message": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized",
                }, 401
        except Exception as e:
            raise e 
        '''{
                "message": "Something went wrong",
                "data": e,
                "error": str(e),
            }, 500'''

        return f(current_user, *args, **kwargs)

    return decorated


@health.get(
    "/",
    summary="Get health status",
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
def get_health():
    return "Ok", 200


@user.get(
    "/",
    summary="Get health status",
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
@token_required
async def get_user(current_user):
    service: TaskService = await get_tasks_service()
    return "Ok", 200


@user.post("/",
            summary="Get health status",
            responses={
                200: {"description": "Successful response"},
                400: {"description": "..."},
            },
            
)
@token_required
@tasks.get(
    "/",
    summary="Get a list of tasks",
    security=security,
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
@token_required
def get_tasks(current_user: domain.User):
    
    return f"{current_user.id}, {current_user.name}, {current_user.admin}" 


@tasks.post(
    "/",
    summary="Create a new task",
    security=security,
    responses={200: {"description": "Successful response"}},
)
@token_required
def create_task(current_user, body: CreateTask):
    return body.title, body.description


@tasks.get(
    "/<int:task_id>",
    summary="Get task details by ID",
    security=security,
    responses={200: {"description": "Successful response"}},
)
@token_required
def get_task(current_user, path: GetTask):
    if not path.task_id:
        return "NotFoundResponse", 404
    return str(path.task_id)


@tasks.put(
    "/<int:task_id>",
    summary="Update task details by ID",
    security=security,
    responses={200: {"description": "Successful response"}},
)
@token_required
def put_task(current_user, path: GetTask, body: UpdateTask):
    if not path.task_id:
        return "NotFoundResponse", 404
    return str(path.task_id)


@tasks.delete(
    "/",
    summary="Update task details by ID",
    security=security,
    responses={200: {"description": "Successful response"}},
)
@token_required
def delete(current_user, path: GetTask):
    ...
