from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from models.enum import UserLoginMethodsTypeEnum


class CreateLoginMethodSchema(BaseModel):
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    active: bool
    verify: bool


class ListLoginMethodsSchema(BaseModel):
    id: UUID
    created: datetime
    code: str
    user_id: UUID
