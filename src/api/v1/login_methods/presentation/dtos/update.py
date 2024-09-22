from uuid import UUID

from pydantic import BaseModel

from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class UpdateLoginMethodDto(BaseModel):
    user_id: UUID | None = None
    entity_id: UUID | None = None
    entity_type: UserLoginMethodsTypeEnum | None = None
    active: bool | None = None
    verify: bool | None = None
