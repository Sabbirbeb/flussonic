from typing import AsyncGenerator

import pytest
from flask_openapi3 import OpenAPI
from sqlalchemy.ext.asyncio import close_all_sessions

from app.application import schemas as dto
from app.application.interface import IUnitOfWork
from app.domain import User
from app.infrastructure.database.models import metadata
from app.infrastructure.database.session import get_database_engine
from app.infrastructure.server import make_app
from app.infrastructure.uow import UnitOfWork


@pytest.fixture(autouse=True)
async def setup_bd() -> AsyncGenerator[None, None]:
    local_async_engine = get_database_engine()
    async with local_async_engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)
        await connection.run_sync(metadata.create_all)
    yield
    await close_all_sessions()
    async with local_async_engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)


@pytest.fixture()
def uow() -> IUnitOfWork:
    return UnitOfWork()


@pytest.fixture()
def app() -> OpenAPI:
    return make_app()


# that doesnt work for asgi idk GL
# total time spend here: 2 hours
# update it by yourself  ^
@pytest.fixture()
def test_client(app) -> OpenAPI:
    # Create a test client using the Flask application
    with app.test_client() as testing_client:
        yield testing_client  # this is where the testing happens!


@pytest.fixture()
async def unregisterd_user() -> User:
    return User(id=666, name='WhoAmI', admin=False)


@pytest.fixture()
async def user(uow: IUnitOfWork) -> User:
    async with uow:
        user = await uow.users.get_by_name("Test")
        if not user:
            user = await uow.users.create(
                dto.UserCreate(name="Test", admin=False),
            )
            await uow.commit()
        return user


@pytest.fixture()
async def admin(uow: IUnitOfWork) -> User:
    async with uow:
        user = await uow.users.get_by_name("test_admin")
        if not user:
            user = await uow.users.create(
                dto.UserCreate(name="test_admin", admin=True),
            )
            await uow.commit()
        return user
