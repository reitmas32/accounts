

from pydantic import BaseModel

from shared.app.entities.list_body import ListBodyEntity
from shared.app.status_code import StatusCodes


class DetailsSchema(BaseModel):
    errors: list = []
    message: str | int
    code: str | int
    trace_id: str
    caller_id: str

class ResponseSchema(BaseModel):
    data: ListBodyEntity | str | dict | None = None
    success: bool
    details: DetailsSchema


class ResponseEntity(BaseModel):
    data: ListBodyEntity | str | dict | None = None
    code: StatusCodes
