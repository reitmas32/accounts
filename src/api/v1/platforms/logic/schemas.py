from pydantic import BaseModel

from api.v1.users.crud.schemas import UserSchema
from shared.app.enums import PlatformsLogin


class SignupPlatformSchema(UserSchema):
    external_id: str
    user_name: str | None = None
    platform: PlatformsLogin
    metadata: dict | None = None
    token: str


class SignInPlatformSchema(BaseModel):
    external_id: str
    platform: PlatformsLogin
    token: str


class TokenData(BaseModel):
    username: str | None = None
