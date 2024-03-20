import pytest

from app.application import schemas
from app.application.interface import IUnitOfWork
from app.domain import TaskStatus, User


class TestTasksRepo:
    async def test_create(self, uow: IUnitOfWork, user: User) -> None:
        async with uow:
            task = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ),
            )
            await uow.commit()

        assert task.id != None  # noqa: E711
        assert task.status == "waiting"
        assert task.title == "test_title"
        assert task.description == "test_description"
        assert task.user_id == user.id

    async def test_get(
        self,
        uow: IUnitOfWork,
        user: User,
    ) -> None:
        async with uow:
            task = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ),
            )
            await uow.commit()
            get_task = await uow.tasks.get(obj_id=task.id)

        assert task.id == get_task.id
        assert task.status == get_task.status
        assert task.title == get_task.title
        assert task.description == get_task.description
        assert task.user_id == get_task.user_id

    async def test_update(
        self,
        uow: IUnitOfWork,
        user: User,
    ) -> None:
        async with uow:
            task = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ),
            )
            await uow.commit()
            get_task = await uow.tasks.update(
                obj_id=task.id,
                update_dto=schemas.TaskUpdate(title="Updated", description="Updated", status=TaskStatus.DECLINED),
            )
            await uow.commit()

        assert task.id == get_task.id
        assert get_task.status == "declined"
        assert get_task.title == "Updated"
        assert get_task.description == "Updated"
        assert get_task.user_id == user.id

    async def test_delete(
        self,
        uow: IUnitOfWork,
        user: User,
    ) -> None:
        async with uow:
            task = await uow.tasks.create(
                schemas.TaskCreate(
                    user_id=user.id,
                    status=TaskStatus.WAITING,
                    title="test_title",
                    description="test_description",
                ),
            )
            await uow.commit()
            get_task = await uow.tasks.delete(obj_id=task.id)
            await uow.commit()

        assert get_task == 0
