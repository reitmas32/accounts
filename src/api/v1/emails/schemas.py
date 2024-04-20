from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateEmailSchema(BaseModel):
    email: str
    user_id: UUID
    password: str


class ListEmailSchema(BaseModel):
    id: UUID
    created: datetime
    email: str
    user_id: UUID
