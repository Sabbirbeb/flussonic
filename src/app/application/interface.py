from abc import ABC, abstractmethod
from types import TracebackType
from typing import Collection, Self

from app import domain
from app.application import schemas


class ITasksRepository(ABC):
    @abstractmethod
    async def bulk_create(
        self, create_dto: list[schemas.TaskCreate]
    ) -> list[domain.Task]:
        ...

    @abstractmethod
    async def create(self, create_dto: schemas.TaskCreate) -> domain.Task:
        ...

    @abstractmethod
    async def get(self, obj_id: int) -> domain.Task | None:
        ...

    @abstractmethod
    async def update(
        self, obj_id: int, update_dto: schemas.TaskUpdate
    ) -> domain.Task | None:
        ...

    @abstractmethod
    async def delete(self, obj_id: int) -> bool | None:
        ...

    @abstractmethod
    async def list_by_batch_id(self, batch_id: int) -> list[domain.Task]:
        ...

    @abstractmethod
    async def list_by_id(self, ids: Collection[int]) -> list[domain.Task]:
        ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[domain.Task]:
        ...


class IUsersRepository(ABC):
    @abstractmethod
    async def bulk_create(
        self, create_dto: list[schemas.TaskCreate]
    ) -> list[domain.Task]:
        ...

    @abstractmethod
    async def create(self, create_dto: schemas.TaskCreate) -> domain.Task:
        ...

    @abstractmethod
    async def get(self, obj_id: int) -> domain.Task | None:
        ...

    @abstractmethod
    async def update(
        self, obj_id: int, update_dto: schemas.TaskUpdate
    ) -> domain.Task | None:
        ...

    @abstractmethod
    async def delete(self, obj_id: int) -> bool | None:
        ...

    @abstractmethod
    async def list_by_batch_id(self, batch_id: int) -> list[domain.Task]:
        ...

    @abstractmethod
    async def list_by_id(self, ids: Collection[int]) -> list[domain.Task]:
        ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[domain.Task]:
        ...


class IUnitOfWork(ABC):
    users: IUsersRepository
    tasks: ITasksRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
