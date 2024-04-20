from uuid import UUID

from core.utils.schema_base import BaseSchema
from models.email import EmailModel


class EmailProxy(EmailModel):
    pass


class RetrieveEmailSchema(BaseSchema):
    user_id: UUID
    email: str
