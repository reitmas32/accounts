from uuid import UUID

from shared.presentation.dtos.base_filter import BaseFilters


class EmailFilters(BaseFilters):
    user_id: UUID | None = None
    email: str | None = None
