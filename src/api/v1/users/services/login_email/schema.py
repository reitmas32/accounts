from pydantic import BaseModel, EmailStr

from core.utils.schema_base import BaseSchema

#################
# Requests
#################


class LoginEmailSchema(BaseModel):
    user_name: str | None = None
    email: EmailStr | None = None
    password: str


#################
# Responses
#################


class RetrieveLoginEmailEmailSchema(BaseSchema):
    user_name: str
    email: str
