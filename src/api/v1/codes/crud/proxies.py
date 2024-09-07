from datetime import datetime
from uuid import UUID

from core.utils.schema_base import BaseSchema
from shared.databases.postgres.models import CodeModel


class CodeProxy(CodeModel):
    pass


class RetrieveCodeSchema(BaseSchema):
    code: str
    user_id: UUID
    entity_id: UUID
    entity_type: str
    type: str
    used_at: datetime
