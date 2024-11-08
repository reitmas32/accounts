from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from core.utils.validations.password import active_validations
from shared.app.errors.invalid.missing_credentials import MissingCredentialsError


class SigninEmailDto(BaseModel):
    user_name: str | None = None
    email: EmailStr | None = None
    password: str = Field(..., example="Password123!")

    @field_validator("password")
    def validate_password(cls, value):  # noqa: N805
        for validation in active_validations:
            if not validation.value.validation_fn(value):
                raise validation.value.error

        return value

    @model_validator(mode="before")
    def check_user_name_or_email(cls, values):  # noqa: N805
        user_name = values.get("user_name")
        email = values.get("email")

        if not user_name and not email:
            raise MissingCredentialsError
        return values
