from enum import StrEnum, auto

# (например, "в ожидании", "в процессе", "завершено") ??  
class EntityStatus(StrEnum):
    WAITING = auto()
    PROCESSING = auto()
    ACCEPTED = auto()
    DECLINED = auto()