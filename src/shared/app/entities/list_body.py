from typing import Any

from pydantic import BaseModel


class ListBodyEntity(BaseModel):
    next: str | None = None
    prev: str | None = None
    count: int | None = None
    data: list[Any]
