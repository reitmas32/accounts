from core.utils.repository_base import RepositoryBase
from models.user_login_methods import UserLoginMethodModel


class RepositoryUserLoginMethod(RepositoryBase):
    """
    Repository for operations related to user login methods.

    This repository provides methods for performing queries and operations on the UserLoginMethodModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the UserLoginMethodModel table.

    Methods:
        No additional methods provided.
    """

    model: UserLoginMethodModel = UserLoginMethodModel
