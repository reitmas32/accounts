from shared.app.entities.base_entity import EntityBase


class RoleEntity(EntityBase):
    name: str
    description: str | None = None
