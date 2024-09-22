from pydantic import BaseModel

from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class JWTSchema(BaseModel):
    user_id: str
    entity_id: str
    entity_type: UserLoginMethodsTypeEnum

