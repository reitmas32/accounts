from core.utils.responses import FilterBaseSchema
from models.enum import CodeTypeEnum, UserLoginMethodsTypeEnum


class FilterCodesSchema(FilterBaseSchema):
    code: str | None = None
    user_id: str | None = None
    entity_id: str | None = None
    entity_type: UserLoginMethodsTypeEnum | None = None
    type: CodeTypeEnum | None = None
    used_at: str | None = None
