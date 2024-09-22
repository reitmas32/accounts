from datetime import date

from pydantic import BaseModel


class CreateUserDto(BaseModel):
    user_name: str | None = None
    name: str | None = None
    birthday: date | None = None
    extra_data: dict | None = None
