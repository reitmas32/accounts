from uuid import UUID

from pydantic import field_serializer

from shared.app.entities.base_entity import EntityBase


class EmailEntity(EntityBase):
    email: str
    user_id: UUID | None = None
    password: str

    @field_serializer("user_id")
    def serialize_user_id(self, value):
        return str(value) if value is not None else None
