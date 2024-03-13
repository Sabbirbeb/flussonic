from dataclasses import dataclass
from enum import StrEnum, auto


# (например, "в ожидании", "в процессе", "завершено") ??
class TaskStatus(StrEnum):
    WAITING = auto()
    PROCESSING = auto()
    ACCEPTED = auto()
    DECLINED = auto()


@dataclass(frozen=True, kw_only=True)
class Task:
    id: int
    title: str
    description: str
    status: TaskStatus
    user_id: int


@dataclass(frozen=True, kw_only=True)
class User:
    id: int
    name: str
    admin: bool
