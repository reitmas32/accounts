from shared.presentation.dtos.base_filter import BaseFilters


class RoleFilters(BaseFilters):
    name: str | None = None
    description: str | None = None
