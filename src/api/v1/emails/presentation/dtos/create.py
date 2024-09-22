from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator

from core.utils.validations.password import active_validations


class CreateEmailDto(BaseModel):
    email: EmailStr
    user_id: UUID
    password: str

    @field_validator("password")
    def validate_password(cls, value):  # noqa: N805
        for validation in active_validations:
            if not validation.value.validation_fn(value):
                raise validation.value.error

        return value
