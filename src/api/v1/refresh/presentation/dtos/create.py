from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreateRefreshTokenDto(BaseModel):
    user_id: UUID
    external_id: UUID
    login_method_id: UUID
    expires_at: datetime
    revoked_at: datetime | None = None
