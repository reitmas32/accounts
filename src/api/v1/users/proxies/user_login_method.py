from core.utils.repository_base import RepositoryBase
from models.login_methods import LoginMethodModel


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
