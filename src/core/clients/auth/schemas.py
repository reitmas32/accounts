from pydantic import BaseModel


class AuthSchema(BaseModel):
    service_name: str
    api_key: str
