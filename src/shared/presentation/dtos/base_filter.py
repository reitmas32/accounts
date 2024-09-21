from pydantic import BaseModel


class BaseFilters(BaseModel):
    ordering: str | None = "created"
