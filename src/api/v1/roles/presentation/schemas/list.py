from shared.app.entities.base_entity import EntityBase


class ListRoleSchema(EntityBase):
    name: str
    description: str | None = None
