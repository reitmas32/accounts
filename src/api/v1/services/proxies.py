from uuid import UUID

from core.utils.schema_base import BaseSchema
from models import ServiceModel


class ServiceProxy(ServiceModel):
    pass

class RetrieveServiceSchema(BaseSchema):
    api_key: UUID
    service_name: str
