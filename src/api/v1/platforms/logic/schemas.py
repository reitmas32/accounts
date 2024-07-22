from pydantic import BaseModel

from api.v1.users.crud.schemas import UserSchema
from models.enum import PlatformsLogin


class SignupPlatformSchema(UserSchema):
    external_token: str
    user_name: str | None = None
    platform: PlatformsLogin
    metadata: dict | None = None


class SignInPlatformSchema(BaseModel):
    external_token: str
    platform: PlatformsLogin


class TokenData(BaseModel):
    username: str | None = None
