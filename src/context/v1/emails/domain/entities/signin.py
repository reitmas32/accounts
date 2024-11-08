from pydantic import BaseModel, EmailStr


class SigninEmailEntity(BaseModel):
    user_name: str | None = None
    email: EmailStr | None = None
    password: str
