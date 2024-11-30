from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from shared.app.entities.base_entity import EntityBase


class RefreshTokenEntity(EntityBase):
    user_id: UUID | str
    login_method_id: UUID | str
    external_id: UUID | str
    expires_at: datetime
    revoked_at: datetime | None = None

class CreateRefreshTokenEntity(BaseModel):
    user_id: UUID | None = None
    login_method_id: UUID | None = None
