from pydantic import BaseModel

from shared.app.enums.code_type import CodeTypeEnum


class ResendCodeEntity(BaseModel):
    email: str
    type: CodeTypeEnum
