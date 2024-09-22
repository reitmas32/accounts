from pydantic import BaseModel

from shared.app.enums.platform_login import PlatformsLogin


class SigninPlatformEntity(BaseModel):
    platform: PlatformsLogin
    external_id: str
    token: str
