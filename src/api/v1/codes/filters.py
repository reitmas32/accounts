from core.utils.responses import FilterBaseSchema


class FilterCodesSchema(FilterBaseSchema):
    code: str | None = None
    user_id: str | None = None
    entity_id: str | None = None
    entity_type: str | None = None
    type: str | None = None
    used_at: str | None = None
