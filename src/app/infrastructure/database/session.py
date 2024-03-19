from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.settings import settings


def get_database_engine() -> AsyncEngine:
    return create_async_engine(
        settings.pg_dsn,
        poolclass=NullPool,
    )


sessionmaker = async_sessionmaker(
    get_database_engine(),
    expire_on_commit=False,
    autoflush=True,
)
