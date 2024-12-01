from pydantic import BaseModel, Field


class CreateRoleDto(BaseModel):
    name: str = Field(..., example="admin")
    description: str | None = None

