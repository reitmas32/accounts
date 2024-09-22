from uuid import UUID

from shared.app.enums.platform_login import PlatformsLogin
from shared.presentation.dtos.base_filter import BaseFilters


class PlatformFilters(BaseFilters):
    user_id: UUID | None = None
    external_id: str | None = None
    active: bool | None = None
    platform: PlatformsLogin | None = None
