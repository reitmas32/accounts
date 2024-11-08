from pydantic import BaseModel, EmailStr


class SignupEmailEntity(BaseModel):
    user_name: str | None = None
    email: EmailStr
    password: str
