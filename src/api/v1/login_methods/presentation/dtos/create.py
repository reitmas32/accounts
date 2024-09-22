from uuid import UUID

from pydantic import BaseModel

from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class CreateLoginMethodDto(BaseModel):
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    active: bool
    verify: bool
