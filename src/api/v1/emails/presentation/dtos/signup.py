from pydantic import BaseModel, EmailStr, Field, field_validator

from core.utils.validations.password import active_validations


class SignupEmailDto(BaseModel):
    user_name: str | None = None
    email: EmailStr
    password: str = Field(..., example="Password123!")

    @field_validator("password")
    def validate_password(cls, value):  # noqa: N805
        for validation in active_validations:
            if not validation.value.validation_fn(value):
                raise validation.value.error

        return value
