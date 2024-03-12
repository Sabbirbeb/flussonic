from sqlalchemy import (
    ForeignKey,
    MetaData,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from app.domain import TaskStatus

metadata = MetaData()

Base = declarative_base(metadata=metadata)


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        default=int,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(nullable=False)

    admin: Mapped[str] = mapped_column(nullable=False, default=False)


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        default=int,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        nullable=False, default=TaskStatus.WAITING
    )

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
