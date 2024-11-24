from datetime import datetime
from uuid import UUID

from shared.presentation.dtos.base_filter import BaseFilters


class RefreshTokenFilters(BaseFilters):
    user_id: UUID | None = None
    external_id: UUID | None = None
    login_method_id: UUID | None = None
    expires_at: datetime | None = None
    revoked_at: datetime | None = None
