
from pydantic import BaseModel, conint


class PaginationParams(BaseModel):
    size: conint(ge=1, le=500) = 30  # type: ignore  # noqa: PGH003
    page: conint(ge=1) = 1  # type: ignore  # noqa: PGH003
