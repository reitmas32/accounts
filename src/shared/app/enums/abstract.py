from enum import StrEnum


class AbstractEnum(StrEnum):
    @classmethod
    def list_values(cls):
        return [member.value for member in cls]
