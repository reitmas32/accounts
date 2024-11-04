from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EntityBase(BaseModel):
    id: UUID | str | None = None
    created: datetime | None = None
    updated: datetime | None = None
    is_removed: bool | None = None

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
