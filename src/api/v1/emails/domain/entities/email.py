from uuid import UUID

from pydantic import field_validator

from shared.app.entities.base_entity import EntityBase
from shared.app.handlers.password import PasswordHandler


class EmailEntity(EntityBase):
    email: str
    user_id: UUID
    password: str

    # Validación posterior a la creación del objeto para encriptar la contraseña
    @field_validator("password", mode="before")
    def hash_password(cls, value):  # noqa: N805
        # Verifica si la contraseña ya está encriptada
        return PasswordHandler.hash_password(password=value)
