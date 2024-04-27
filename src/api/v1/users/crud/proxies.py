from sqlalchemy import desc, or_, select

from core.utils.repository_base import RepositoryBase
from models import (
    UserModel,
)


class RepositoryUser(RepositoryBase):
    """
    Repository for operations related to user management.

    This repository provides methods for performing queries and operations on the UserModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the UserModel table.

    Methods:
        exists_email_or_user_name: Checks if a user with the given email or username exists.
        get_user: Retrieves a user record associated with the given username.
        get_last_user_with_specifi_email: Retrieves the last user registered with the specified email.
    """

    model = UserModel

    def exists_email_or_user_name(self, email: str, user_name: str) -> bool:
        """
        Checks if a user with the given email or username exists.

        Args:
            email (str): Email to check.
            user_name (str): Username to check.

        Returns:
            bool: True if a user with the given email or username exists, False otherwise.
        """
        query = select(self.model).where(or_(self.model.email == email, self.model.user_name == user_name))
        result = self.session.execute(query).first()
        return result is not None

    def get_user(self, user_name: str) -> UserModel:
        """
        Retrieves a user record associated with the given username.

        Args:
            user_name (str): Username associated with the user record.

        Returns:
            UserModel: User record associated with the given username, or None if not found.
        """
        query = select(self.model).where(self.model.user_name == user_name)
        result = self.session.execute(query).first()
        return result[0] if result else None

    def get_last_user_with_specifi_email(self, email: str) -> UserModel:
        """
        Retrieves the last user registered with the specified email.

        Args:
            email (str): Email associated with the user.

        Returns:
            UserModel: Last user registered with the specified email, or None if not found.
        """
        query = select(self.model).where(self.model.email == email).order_by(desc(self.model.created))
        result = self.session.execute(query).first()
        return result[0] if result else None
