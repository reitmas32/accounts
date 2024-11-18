

from pydantic import BaseModel

from shared.app.status_code import StatusCodes


class DetailsSchema(BaseModel):
    errors: list[str] = []
    message: str
    code: str
    trace_id: str
    caller_id: str

class ResponseSchema(BaseModel):
    data: str | dict | None = None
    success: bool
    details: DetailsSchema


class ResponseEntity(BaseModel):
    data: str | dict | None = None
    code: StatusCodes
