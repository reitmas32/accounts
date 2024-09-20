from pydantic import BaseModel


class JWTSchema(BaseModel):
    user_id: str
