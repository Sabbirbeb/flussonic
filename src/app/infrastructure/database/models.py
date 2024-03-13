from sqlalchemy import (
    Column,
    ForeignKey,
    MetaData,
    Integer,
    String,
    Boolean
)
from sqlalchemy.orm import declarative_base

from app.domain import TaskStatus

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    admin = Column(Boolean)


class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    status = Column(String, nullable=False, default=TaskStatus.WAITING)

    user_id = Column(ForeignKey("users.id"), nullable=False)
