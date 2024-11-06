from pydantic import BaseModel

from shared.app.enums.platform_login import PlatformsLogin


class SignupPlatformEntity(BaseModel):
    platform: PlatformsLogin
    external_id: str
    token: str
    user_name: str | None = None
    metadata: dict | None = None
