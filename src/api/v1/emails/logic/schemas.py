from pydantic import BaseModel, EmailStr

from api.v1.users.crud.schemas import UserSchema
from core.utils.schema_base import BaseSchema


class SignupEmailSchema(UserSchema):
    email: EmailStr
    password: str


class LoginEmailSchema(BaseModel):
    user_name: str | None = None
    email: EmailStr | None = None
    password: str

class RetrieveSingUpEmailSchema(BaseSchema):

    user_name: str
    email: str

class VerifyEmailSchema(BaseModel):
    user_name: str
    code: str
