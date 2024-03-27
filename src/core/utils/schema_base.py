from uuid import UUID
from pydantic import BaseModel
from datetime import datetime

class BaseSchema(BaseModel):
    id: UUID
    updated : datetime
    created : datetime