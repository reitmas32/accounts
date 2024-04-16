from sqlalchemy import select

from core.utils.repository_base import RepositoryBase
from models import (
    AuthGeneralPlatformModel,
)


class RepositoryAuthGeneralPlatform(RepositoryBase):
    """
    Repository for operations related to general platform authentication.

    This repository provides methods for performing queries and operations on the AuthGeneralPlatformModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the AuthGeneralPlatformModel table.

    Methods:
        get_auth_platform: Retrieves an AuthGeneralPlatformModel record associated with the given hashed platform ID and type.
    """

    model = AuthGeneralPlatformModel

    def get_auth_platform(self, hashed_platform_id: str, type: AuthGeneralPlatformModel) -> AuthGeneralPlatformModel:
        """
        Retrieves an AuthGeneralPlatformModel record associated with the given hashed platform ID and type.

        Args:
            hashed_platform_id (str): Hashed platform ID associated with the record.
            type (AuthGeneralPlatformModel): Type of the platform.

        Returns:
            AuthGeneralPlatformModel: AuthGeneralPlatformModel record associated with the given hashed platform ID and type, or None if not found.
        """
        query = select(self.model).where(self.model.hashed_platform_id == hashed_platform_id, self.model.type == type)
        result = self.session.execute(query).first()
        return result[0] if result else None
