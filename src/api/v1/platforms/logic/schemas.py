from pydantic import BaseModel

from api.v1.users.crud.schemas import UserSchema
from models.enum import PlatformsLogin


class SignupPlatformSchema(UserSchema):
    id_user: str
    user_name: str | None = None
    platform: PlatformsLogin
    metadata: dict | None = None


class SignInPlatformSchema(BaseModel):
    id_user: str
    platform: PlatformsLogin
