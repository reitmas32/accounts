from pydantic import BaseModel


class UpdateRoleDto(BaseModel):
    name: str | None = None
    description: str | None = None
