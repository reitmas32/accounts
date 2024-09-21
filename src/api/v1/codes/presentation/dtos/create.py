from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from shared.app.enums.code_type import CodeTypeEnum
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum


class CreateCodeDto(BaseModel):
    code: str
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    type: CodeTypeEnum
    used_at: datetime | None = None
