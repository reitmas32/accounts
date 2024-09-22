from uuid import UUID

from pydantic import BaseModel

from shared.app.enums.platform_login import PlatformsLogin


class CreatePlatformDto(BaseModel):
    user_id: UUID
    external_id: str
    active: bool = False
    platform: PlatformsLogin
