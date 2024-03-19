import abc
from typing import Any, Collection, Generic, Never, Self, Type, TypeVar
from uuid import UUID

from sqlalchemy import Result, Select, delete, exc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app import domain
from app.application import errors
from app.application.interface import ITasksRepository, IUsersRepository
from app.application.logger import log
from app.infrastructure.database import models

T = TypeVar("T")
M = TypeVar("M")


class SqlRepository(abc.ABC, Generic[T, M]):
    model: Type[M]  # noqa: FA100

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @classmethod
    @abc.abstractmethod
    def map(cls: type[Self], obj: M) -> T:
        ...

    @log
    async def bulk_create(self, create_dtos: list[Any]) -> list[T]:
        try:
            query: Any = insert(self.model).values([dto.model_dump() for dto in create_dtos]).returning(self.model)
            result = await self.session.execute(query)

            objects = result.scalars().all()
        except exc.IntegrityError as e:
            raise errors.MutationConflictError(e)

        return [self.map(obj) for obj in objects]

    @log
    async def create(self, create_dto: Any) -> T:  # noqa: ANN401
        try:
            cmd = insert(self.model).values(create_dto.model_dump()).returning(self.model)
            result = await self.session.execute(cmd)

            obj = result.scalar_one()
        except exc.IntegrityError as e:
            raise errors.MutationConflictError(e)
        return self.map(obj)

    @log
    async def get(self, obj_id: UUID | str) -> T | None:
        query = select(self.model).filter_by(id=obj_id)
        result = await self.session.execute(query)
        obj = result.scalar_one_or_none()
        if not obj:
            return None

        return self.map(obj)

    @log
    async def update(self, obj_id: UUID | str, update_dto: Any) -> T | None:  # noqa: ANN401
        try:
            cmd = (
                update(self.model)
                .where(self.model.id == obj_id)  # type: ignore
                .values(update_dto.model_dump(exclude_unset=True))
                .returning(self.model)
            )
            result = await self.session.execute(cmd)

            obj = result.scalar_one_or_none()
        except exc.IntegrityError as e:
            raise errors.MutationConflictError(e)
        if not obj:
            return None

        return self.map(obj)

    @log
    async def list_by_id(self, ids: Collection[UUID | str]) -> list[T]:
        query: Select[tuple[Never]] = select(self.model).where(self.model.id.in_(ids))  # type: ignore
        result: Result[tuple[M]] = await self.session.execute(query)
        return [self.map(obj) for obj in result.scalars()]

    @log
    async def list(self) -> list[T]:
        query = select(self.model)
        result = await self.session.execute(query)

        return [self.map(obj) for obj in result.scalars()]

    @log
    async def delete(self, obj_id: int) -> T | None:
        query = delete(self.model).where(self.model.id == obj_id)
        await self.session.execute(query)

        return 0


class TasksRepository(SqlRepository[domain.Task, models.Tasks], ITasksRepository):
    model = models.Tasks

    @classmethod
    def map(cls: type[Self], task: models.Tasks) -> domain.Task:
        return domain.Task(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            user_id=task.user_id,
        )

    @log
    async def list_by_user_id(self, user_id: str) -> list[domain.Task]:
        query = select(self.model).filter(user_id=user_id)
        result = await self.session.execute(query)

        return [self.map(obj) for obj in result.scalars()]


class UsersRepository(SqlRepository[domain.User, models.Users], IUsersRepository):
    model = models.Users

    @classmethod
    def map(cls: type[Self], user: models.Users) -> domain.User:
        return domain.User(
            id=user.id,
            name=user.name,
            admin=user.admin,
        )

    @log
    async def get_by_name(self, name: str) -> list[domain.User]:
        query = select(self.model).filter_by(name=name)
        result = await self.session.execute(query)

        obj = result.scalar()
        if not obj:
            return None
        return self.map(obj)
