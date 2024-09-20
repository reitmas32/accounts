from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EntityBase(BaseModel):
    id: UUID
    created: datetime
    updated: datetime
    is_removed: bool

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
