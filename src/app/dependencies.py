from app.application.service import TaskService
from app.infrastructure.uow import UnitOfWork


async def get_tasks_service() -> TaskService:
    uow = UnitOfWork()
    service: TaskService = TaskService(uow=uow)
    return service