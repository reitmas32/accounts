from datetime import datetime
from uuid import UUID

from core.utils.schema_base import BaseSchema
from models.login_methods import LoginMethodModel


class LoginMethodsProxy(LoginMethodModel):
    pass


class RetrieveLoginMethodSchema(BaseSchema):
    code: str
    user_id: UUID
    entity_id: UUID
    entity_type: str
    type: str
    used_at: datetime
