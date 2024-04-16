from pydantic import BaseModel


class VerifyEmailSchema(BaseModel):
    user_name: str
    code: str
