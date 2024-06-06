from enum import StrEnum


class MethodType(StrEnum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"


class ReturnType(StrEnum):
    FULL = "full"
    PROCESSED = "processed"
