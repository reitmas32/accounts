from pydantic import BaseModel, EmailStr

from shared.app.enums.code_type import CodeTypeEnum


class ResendCodeDto(BaseModel):
    email: EmailStr
    type: CodeTypeEnum = CodeTypeEnum.ACCOUNT_ACTIVATION
