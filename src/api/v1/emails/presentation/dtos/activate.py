from pydantic import BaseModel, EmailStr, Field, field_validator

from core.settings import settings
from shared.app.errors.code_len import CodeLenError


class ActivateEmailDto(BaseModel):
    email: EmailStr
    code: str = Field(..., example="123456")

    @field_validator("code")
    def validate_code(cls, value):  # noqa: N805
        if len(value) != settings.LENGHT_CODE_VALIDATE_EMAIL:
            raise CodeLenError
        return value
