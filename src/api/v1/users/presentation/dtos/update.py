from datetime import date

from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    user_name: str | None = None
    name: str | None = None
    birthday: date | None = None
    extra_data: dict | None = None
