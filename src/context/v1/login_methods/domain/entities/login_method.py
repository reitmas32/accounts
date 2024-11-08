from uuid import UUID

from shared.app.entities.base_entity import EntityBase
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class LoginMethodEntity(EntityBase):
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    active: bool = False
    verify: bool = False
