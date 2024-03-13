import json

from flask import request
from flask_openapi3 import APIBlueprint, Tag

from functools import wraps

from app import domain
from app.application.service import TaskService
from app.application.schemas import UserCreate, UserUpdate
from app.application import errors
from app.dependencies import get_tasks_service
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
            current_user = request.headers["Authorization"].split(" ")[1]
        if not current_user:
            return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized",
            }, 403
        return await f(current_user, *args, **kwargs)

    return decorated


def token_required_registrated(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        current_user = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        try:
            service = await get_tasks_service()
            async with service.uow as uow:
                current_user= await uow.users.get_by_name(token)
            if not current_user:
                return {
                    "message": "Invalid Authentication token! Registration first!",
                    "data": None,
                    "error": "Unauthorized",
                }, 403
        except Exception as e:
            {
                "message": "Something went wrong",
                "data": e,
                "error": str(e),
            }, 500

        return await f(current_user.id, *args, **kwargs)

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
    summary="Update user to admin status",
    security=security,
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
@token_required_registrated
async def make_user_admin(current_user_id):
    service: TaskService = await get_tasks_service()
    async with service.uow as uow:
        user = await uow.users.update(obj_id=current_user_id,
                                      update_dto=UserUpdate(admin=True))
        await uow.commit()
    return f"{user.id}, {user.name}, admin={user.admin}"


@user.post("/",
            summary="Registrate user",
            security=security,
            responses={
                200: {"description": "Successful response"},
                400: {"description": "..."},
            },
            
)
@token_required
async def registrate_user(current_user: domain.User):
    service: TaskService = await get_tasks_service()
    try:
        user = await service.get_user_by_name(current_user)
    except errors.NotFoundError :
        user = await service.create_user(UserCreate(name=current_user,
                                                    admin=False))

    return json.dumps({
                        'id':user.id,
                        'name':user.name,
                        'admin':user.admin
                    },
                    indent=2)


@user.get("/list",
            summary="List users",
            security=security,
            responses={
                200: {"description": "Successful response"},
                400: {"description": "..."},
            },
            )
@token_required_registrated
async def get_users(current_user):
    service: TaskService = await get_tasks_service()
    users = await service.get_users()
    return json.dumps([{
            'id':user.id,
            'name':user.name,
            'admin':user.admin
        }
        for user in users
        ], indent=2)

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
