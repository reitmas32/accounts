from uuid import UUID

from sqlalchemy import and_, or_, select

from api.v1.platforms.logic.schemas import PlatformsLogin
from core.utils.repository_base import RepositoryBase
from models import (
    AuthGeneralPlatformModel,
    UserModel,
)


class RepositoryPlatformUser(RepositoryBase):
    """
    Repository for operations related to email authentication.

    This repository provides methods for performing queries and operations on the EmailModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the EmailModel table.

    Methods:
        exists_email: Checks if a record with the given email exists.
        get_auth_email: Retrieves an EmailModel record associated with the given email.
        get_last_user_with_specifi_email: Retrieves the last user registered with the given email.
    """

    model = AuthGeneralPlatformModel

    def exists_id_of_platform(
        self,
        hashed_platform_id: str,
        platform: PlatformsLogin,
        user_id: UUID,
    ) -> bool:
        """
        Checks if a record with the given email exists.

        Args:
            email (str): Email to check.

        Returns:
            bool: True if a record with the given email exists, False otherwise.
        """
        query = select(self.model).where(
            or_(
                and_(
                    self.model.hashed_platform_id == hashed_platform_id,
                    self.model.type == platform,
                ),
                and_(
                    self.model.user_id == user_id,
                    self.model.type == platform,
                ),
            )
        )
        result = self.session.execute(query).first()
        return result is not None

    def get_platform_by_user_id(self, user_id: str, platform: PlatformsLogin) -> UserModel:
        """
        Retrieves an EmailModel record associated with the given email.

        Args:
            email (str): Email associated with the record.

        Returns:
            UserModel: User record associated with the given email, or None if not found.
        """
        platforms = self.get_by_attributes(user_id=user_id, type=platform)
        if len(platforms) == 0:
            return None
        return platforms[0]
