from uuid import UUID

from shared.app.entities.base_entity import EntityBase


class SignupEmailSchema(EntityBase):
    email: str
    user_id: UUID | None = None
