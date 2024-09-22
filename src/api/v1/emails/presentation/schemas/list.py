from uuid import UUID

from shared.app.entities.base_entity import EntityBase


class ListEmailSchema(EntityBase):
    user_id: UUID
    email: str
