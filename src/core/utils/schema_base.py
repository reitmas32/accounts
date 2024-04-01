from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: UUID
    updated : datetime
    created : datetime
