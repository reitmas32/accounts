from uuid import UUID
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Dict,Optional
from core.utils.schema_base import BaseSchema
from models.enum import UserAuthMethodEnum,UserActivationMethodEnum
from pydantic import BaseModel, validator
import phonenumbers
from typing import Optional


class ListUserSchema(BaseModel):
    id: UUID
    user_name: str
    email: EmailStr

 
class RetrieveUserServiceSchema(BaseSchema):
    email: EmailStr
    user_name: str
    validate: bool
    auth_method_default : Optional[UserAuthMethodEnum] = None
    activation_method : Optional[UserActivationMethodEnum] = None
    extra_data : Optional[Dict] = None
    phone_number: Optional[str] = None

    @validator('phone_number', pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):
        if v is not None:
            try:
                number = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(number):
                    raise ValueError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        return v
    
class CreateUserSchema(BaseModel):
    email: EmailStr
    password: str
    user_name: str
    extra_data : Optional[Dict] = None
    phone_number: Optional[str] = None

    @validator('phone_number', pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):
        if v is not None:
            try:
                number = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(number):
                    raise ValueError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        return v
    

class ActivateAccountUserSchema(BaseModel):
    email: EmailStr
    code: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str
    code: Optional[str] = None
    auth_method : Optional[UserAuthMethodEnum] = None


class ValidateTokenSchema(BaseModel):
    token: str