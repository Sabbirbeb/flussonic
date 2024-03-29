# fastapi > flask??? https://habr.com/ru/articles/748618/
import json
from functools import wraps
from typing import TYPE_CHECKING

from flask import Response, request
from flask_openapi3 import APIBlueprint, Tag

from app import domain
from app.application import errors
from app.application.schemas import TaskCreate, User, UserCreate
from app.dependencies import get_tasks_service
from app.transport.schemas import CreateTask, GetTask, UpdateTask

if TYPE_CHECKING:
    from app.application.service import TaskService

health_tag = Tag(name="health", description="Health")
health = APIBlueprint(
    "/api/v1/health",
    import_name=__name__,
    url_prefix="/api/v1/health",
    abp_tags=[health_tag],
)

tasks_tag = Tag(name="tasks", description="Tasks")
tasks = APIBlueprint(
    "/api/v1/tasks",
    import_name=__name__,
    url_prefix="/api/v1/tasks",
    abp_tags=[tasks_tag],
)

user_tag = Tag(name="user", description="User")
user = APIBlueprint("/api/v1/user", import_name=__name__, url_prefix="/api/v1/user", abp_tags=[user_tag])

security = [
    {"jwt": []},
]


def token_required(f) -> Response:  # noqa: ANN001
    @wraps(f)
    async def decorated(*args: list, **kwargs: dict) -> Response:
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


def token_required_registrated(f) -> Response:  # noqa: ANN001
    @wraps(f)
    async def decorated(*args: list, **kwargs: dict) -> Response:
        current_user = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        else:
            return {
                "message": "No Bearer token!",
                "data": None,
                "error": "Unauthorized",
            }, 403
        try:
            service = await get_tasks_service()
            async with service.uow as uow:
                current_user = await uow.users.get_by_name(token)
            if not current_user:
                return {
                    "message": "Invalid Authentication token! Registration first!",
                    "data": None,
                    "error": "Unauthorized",
                }, 403
        except Exception as e:  # noqa: BLE001
            return {
                "message": "Something went wrong",
                "data": e,
                "error": str(e),
            }, 500

        print (User(id=current_user.id, name=current_user.name, admin=current_user.admin))
        return await f(
            User(id=current_user.id, name=current_user.name, admin=current_user.admin),
            *args,
            **kwargs,
        )

    return decorated


@health.get(
    "/",
    summary="Get health status",
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
def get_health() -> Response:
    return Response("Ok", status=200)


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
async def make_user_admin(user: User) -> Response:
    service: TaskService = await get_tasks_service()
    user = await service.update_user_to_admin(user=user)
    return json.dumps({"id": user.id, "name": user.name, "admin": user.admin}, indent=2)


@user.post(
    "/",
    summary="Registrate user",
    security=security,
    responses={
        201: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
@token_required
async def registrate_user(current_user: domain.User) -> Response:
    service: TaskService = await get_tasks_service()
    try:
        user = await service.get_user_by_name(current_user)
    except errors.NotFoundError:
        user = await service.create_user(UserCreate(name=current_user, admin=False))

    return json.dumps({"id": user.id, "name": user.name, "admin": user.admin}, indent=2)


@user.get(
    "/list",
    summary="List users",
    security=security,
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
@token_required_registrated
async def get_users(current_user: User) -> Response:  # noqa: ARG001
    service: TaskService = await get_tasks_service()
    users = await service.get_users()
    return json.dumps(
        [{"id": user.id, "name": user.name, "admin": user.admin} for user in users],
        indent=2,
    )


@tasks.get(
    "/",
    summary="Get a list of tasks",
    security=security,
    responses={
        200: {"description": "Successful response"},
        400: {"description": "..."},
    },
)
@token_required_registrated
async def get_tasks(current_user: User) -> Response:  # noqa: ARG001
    service: TaskService = await get_tasks_service()
    tasks = await service.get_tasks()
    return json.dumps(
        [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "user_id": task.user_id,
            }
            for task in tasks
        ],
        indent=2,
    ), 200


@tasks.post(
    "/",
    summary="Create a new task",
    security=security,
    responses={201: {"description": "Task created successfully"}},
)
@token_required_registrated
async def create_task(current_user: User, body: CreateTask) -> Response:
    print (body)
    service: TaskService = await get_tasks_service()
    print (body.title, body.description, current_user.id)
    print (TaskCreate(title=body.title, description=body.description, user_id=current_user.id))
    task = await service.create_task(
        TaskCreate(title=body.title, description=body.description, user_id=current_user.id),
    )
    return json.dumps(
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
        },
        indent=2,
    ), 201


@tasks.get(
    "/<int:task_id>",
    summary="Get task details by ID",
    security=security,
    responses={200: {"description": "Successful response"}},
)
@token_required_registrated
async def get_task(current_user: User, path: GetTask) -> Response:  # noqa: ARG001
    service: TaskService = await get_tasks_service()
    try:
        task = await service.get_task(task_id=path.task_id)
    except errors.NotFoundError:
        return "NotFoundResponse", 404
    return json.dumps(
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
        },
        indent=2,
    ), 200


@tasks.put(
    "/<int:task_id>",
    summary="Update task details by ID",
    security=security,
    responses={200: {"description": "Task updated successfully"}},
)
@token_required_registrated
async def put_task(current_user: User, path: GetTask, body: UpdateTask) -> Response:
    service: TaskService = await get_tasks_service()
    try:
        task = await service.update_task(
            path.task_id,
            UpdateTask(title=body.title, description=body.description, status=body.status),
            user=current_user,
        )
    except errors.NotFoundError:
        return "NotFoundResponse", 404
    except errors.NoPermissionError:
        return "NoPermissionResponse", 403
    return json.dumps(
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
        },
        indent=2,
    ), 200


@tasks.delete(
    "/<int:task_id>",
    summary="Delete a task by ID",
    security=security,
    responses={204: {"description": "Task deleted successfully"}},
)
@token_required_registrated
async def delete(current_user: User, path: GetTask) -> Response:
    service: TaskService = await get_tasks_service()
    try:
        task = await service.delete_task(path.task_id, user=current_user)
    except errors.NotFoundError:
        return "NotFoundResponse", 404
    except errors.NoPermissionError:
        return "NoPermissionResponse", 403
    return json.dumps(
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": task.user_id,
        },
        indent=2,
    ), 204
