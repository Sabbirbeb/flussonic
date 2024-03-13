from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import settings

engine = create_async_engine(
    settings.pg_dsn,
    poolclass=NullPool,
)

sessionmaker = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=True,
)
