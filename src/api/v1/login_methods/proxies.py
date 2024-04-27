from datetime import datetime
from uuid import UUID

from core.utils.repository_base import RepositoryBase
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


class RepositoryUserLoginMethod(RepositoryBase):
    """
    Repository for operations related to user login methods.

    This repository provides methods for performing queries and operations on the LoginMethodModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the LoginMethodModel table.

    Methods:
        No additional methods provided.
    """

    model: LoginMethodModel = LoginMethodModel
