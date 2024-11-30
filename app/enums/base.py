from enum import Enum


class BaseEnum(str, Enum):
    @classmethod
    def values(cls) -> list:
        return list(map(lambda item: item.value, cls))  # type: ignore
