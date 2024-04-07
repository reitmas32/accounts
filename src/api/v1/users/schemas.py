from uuid import UUID

import phonenumbers
from pydantic import BaseModel, EmailStr, validator

from core.utils.schema_base import BaseSchema
from models.enum import AuthGeneralPlatformsEnum, UserAuthMethodEnum


class ListUserSchema(BaseModel):
    id: UUID
    user_name: str
    email: EmailStr


class RetrieveUserSchema(BaseSchema):
    user_name: str
    phone_number: str | None = None
    extra_data: dict | None = None


class CreateUserAuthPlatformSchema(BaseModel):
    signature: str
    user_name: str
    platform_id: str
    type: AuthGeneralPlatformsEnum
    email: EmailStr | None = None
    token: str | None = None
    phone_number: str | None = None
    extra_data: dict | None = None

    @staticmethod
    @validator("phone_number", pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):  # noqa: ARG004
        if v is not None:
            try:
                number = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(number):
                    raise ValueError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        return v


class CreateUserAuthEmailSchema(BaseModel):
    signature: str
    user_name: str
    email: EmailStr
    password: str
    phone_number: str | None = None
    extra_data: dict | None = None

    @staticmethod
    @validator("phone_number", pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):  # noqa: ARG004
        if v is not None:
            try:
                number = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(number):
                    raise ValueError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        return v


class ResponseCreateUserAuthEmailSchema(BaseModel):
    user: RetrieveUserSchema
    token: str


class ActivateAccountUserSchema(BaseModel):
    email: EmailStr
    code: str


class LoginAuthGeneralPlatformSchema(BaseModel):
    signature: str
    platform_id: str
    type: AuthGeneralPlatformsEnum
    token: str | None = None
    email: EmailStr | None = None
    extra_data: dict | None = None


class LoginAuthEmailSchema(BaseModel):
    signature: str
    email: EmailStr
    password: str
    code: str | None = None
    auth_method: UserAuthMethodEnum | None = None


class ValidateTokenSchema(BaseModel):
    token: str
