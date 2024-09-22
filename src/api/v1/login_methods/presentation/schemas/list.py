from uuid import UUID

from shared.app.entities.base_entity import EntityBase
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class ListLoginMethodSchema(EntityBase):
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
