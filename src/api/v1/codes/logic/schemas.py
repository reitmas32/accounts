from uuid import UUID

from pydantic import BaseModel

from models.enum import CodeTypeEnum, UserLoginMethodsTypeEnum


class CreateCodeSchema(BaseModel):
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    type: CodeTypeEnum


class ResentCodeSchema(BaseModel):
    user_id: UUID
    entity_id: UUID
    entity_type: UserLoginMethodsTypeEnum
    type: CodeTypeEnum
