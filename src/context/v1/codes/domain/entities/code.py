from datetime import datetime
from uuid import UUID

from shared.app.entities.base_entity import EntityBase
from shared.app.enums.code_type import CodeTypeEnum
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class CodeEntity(EntityBase):
    code: str
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    type: CodeTypeEnum
    used_at: datetime | None = None
