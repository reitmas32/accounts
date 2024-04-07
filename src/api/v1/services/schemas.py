
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateServiceSchema(BaseModel):
    service_name: str

class ListServiceSchema(BaseModel):
    id: UUID
    created: datetime
    service_name: str
