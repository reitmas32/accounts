from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateCodeSchema(BaseModel):
    code: str
    user_id: str
    entity_id: str
    entity_type: str
    type: str

class ListCodeSchema(BaseModel):
    id: UUID
    created: datetime
    code: str
    user_id: UUID
