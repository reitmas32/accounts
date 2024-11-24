from pydantic import BaseModel


class NewJWTSchema(BaseModel):
    jwt: str
