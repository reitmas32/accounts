from datetime import date

from shared.app.entities.base_entity import EntityBase


class UserEntity(EntityBase):
    user_name: str
    name: str | None = None
    birthday: date | None = None
    extra_data: dict | None = None
