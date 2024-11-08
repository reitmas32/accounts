from pydantic import BaseModel, EmailStr, Field


class ActivateEmailEntity(BaseModel):
    email: EmailStr
    code: str = Field(..., example="123456")
