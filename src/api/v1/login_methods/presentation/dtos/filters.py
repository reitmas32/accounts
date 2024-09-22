from uuid import UUID

from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum
from shared.presentation.dtos.base_filter import BaseFilters


class LoginMethodFilters(BaseFilters):
    user_id: UUID | None = None
    entity_id: UUID | None = None
    entity_type: UserLoginMethodsTypeEnum | None = None
    active: bool | None = None
    verify: bool | None = None
