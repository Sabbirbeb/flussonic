from types import TracebackType
from typing import TYPE_CHECKING, Self

from app.application.interface import IUnitOfWork
from app.infrastructure.database.repository import (
    TasksRepository,
    UsersRepository,
)
from app.infrastructure.database.session import sessionmaker

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        super().__init__()

    async def __aenter__(self) -> Self:
        self._session: AsyncSession = sessionmaker()
        self.tasks = TasksRepository(self._session)
        self.users = UsersRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await super().__aexit__(exc_type, exc, tb)
        await self._session.close()

    async def rollback(self) -> None:
        await self.broker.rollback()
        await self._session.rollback()

    async def commit(self) -> None:
        await self.broker.commit()
        await self._session.commit()
