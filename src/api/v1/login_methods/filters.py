from core.utils.responses import FilterBaseSchema
from shared.app.enums import UserLoginMethodsTypeEnum


class FilterLoginMethodSchema(FilterBaseSchema):
    user_id: str | None = None
    entity_id: str | None = None
    entity_type: UserLoginMethodsTypeEnum | None = None
    active: bool | None = None
    verify: bool | None = None
