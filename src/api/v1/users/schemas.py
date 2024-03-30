from uuid import UUID
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Dict,Optional
from core.utils.schema_base import BaseSchema
from models.enum import UserAuthMethodEnum,AuthGeneralPlatformsEnum
from pydantic import BaseModel, validator
import phonenumbers
from typing import Optional


class ListUserSchema(BaseModel):
    id: UUID
    user_name: str
    email: EmailStr

 
class RetrieveUserSchema(BaseSchema):
    user_name: str
    phone_number: Optional[str] = None
    extra_data : Optional[Dict] = None
    
class CreateUserAuthPlatformSchema(BaseModel):
    signature : str
    user_name: str
    platform_id : str
    type: AuthGeneralPlatformsEnum
    email: Optional[EmailStr] = None
    token : Optional[str] = None
    phone_number: Optional[str] = None
    extra_data : Optional[Dict] = None
    

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
    
class CreateUserAuthEmailSchema(BaseModel):
    signature : str
    user_name: str
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    extra_data : Optional[Dict] = None

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

class ResponseCreateUserAuthEmailSchema(BaseModel):
    user : RetrieveUserSchema
    token : str

class ActivateAccountUserSchema(BaseModel):
    email: EmailStr
    code: str

class LoginAuthGeneralPlatformSchema(BaseModel):
    signature : str
    platform_id : str
    type: AuthGeneralPlatformsEnum
    token : Optional[str] = None
    email: Optional[EmailStr] = None
    extra_data : Optional[Dict] = None
    
class LoginAuthEmailSchema(BaseModel):
    signature : str
    email: EmailStr
    password: str
    code: Optional[str] = None
    auth_method : Optional[UserAuthMethodEnum] = None

class ValidateTokenSchema(BaseModel):
    token: str



class ValidateTokenSchema(BaseModel):
    token: str