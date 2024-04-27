from core.utils.responses import FilterBaseSchema


class FilterEmailsSchema(FilterBaseSchema):
    user_id: str | None = None
    email: str | None = None
