from shared.presentation.dtos.base_filter import BaseFilters


class UserFilters(BaseFilters):
    user_name: str | None = None
    name: str | None = None
    birthday: str | None = None
