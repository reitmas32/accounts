from uuid import UUID

from shared.app.entities.base_entity import EntityBase


class ListCodeSchema(EntityBase):
    code: str
    user_id: UUID
    entity_id: UUID
