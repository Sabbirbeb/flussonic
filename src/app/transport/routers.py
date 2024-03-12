from flask import request
from flask_openapi3 import APIBlueprint, Tag

from functools import wraps 

from app.transport.schemas import CreateTask, GetTask

tasks_tag = Tag(name='tasks', description='Tasks')
tasks = APIBlueprint('/tasks', import_name=__name__, url_prefix='/tasks', abp_tags=[tasks_tag])

security = [
    {"jwt": []},
    ]


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user = None
        if "Authorization" in request.headers:
            current_user = request.headers["Authorization"].split(" ")[1]
        try:
            if not current_user:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated


@tasks.get('/', summary='Get a list of tasks',
           security=security,
           responses={200: {"description": "Successful response"},
                        400: {"description": "..."}})
@token_required
def get_tasks(current_user):
    return current_user


@tasks.post('/', summary='Create a new task',
            security=security,
            responses={200: {"description": "Successful response"}})
@token_required
def create_task(current_user, body: CreateTask):
    return body.name


@tasks.get('/<int:task_id>', summary='Get task details by ID',
            security=security,
            responses={200: {"description": "Successful response"}})
@token_required
def get_task(current_user, path: GetTask):
    if not path.task_id:
        return "NotFoundResponse", 404
    return str(path.task_id)


@tasks.put('/<int:task_id>', summary='Update task details by ID',
            security=security,
            responses={200: {"description": "Successful response"}})
@token_required
def put_task(current_user, path: GetTask, body: CreateTask):
    if not path.task_id:
        return "NotFoundResponse", 404
    return str(path.task_id)

