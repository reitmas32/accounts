from core.utils.responses import FilterBaseSchema


class FilterServicesSchema(FilterBaseSchema):
    service_name: str | None = None
