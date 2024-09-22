from uuid import UUID

from pydantic import BaseModel

from shared.app.enums.platform_login import PlatformsLogin


class UpdatePlatformDto(BaseModel):
    user_id: UUID | None = None
    external_id: str | None = None
    active: bool | None = None
    type: PlatformsLogin | None = None
