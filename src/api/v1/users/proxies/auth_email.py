from sqlalchemy import desc, or_, select

from core.utils.repository_base import RepositoryBase
from models import (
    EmailModel,
    UserModel,
)


class RepositoryEmail(RepositoryBase):
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

    model = EmailModel

    def exists_email(self, email: str) -> bool:
        """
        Checks if a record with the given email exists.

        Args:
            email (str): Email to check.

        Returns:
            bool: True if a record with the given email exists, False otherwise.
        """
        query = select(self.model).where(or_(self.model.email == email))
        result = self.session.execute(query).first()
        return result is not None

    def get_auth_email(self, email: str) -> UserModel:
        """
        Retrieves an EmailModel record associated with the given email.

        Args:
            email (str): Email associated with the record.

        Returns:
            UserModel: User record associated with the given email, or None if not found.
        """
        query = select(self.model).where(self.model.email == email)
        result = self.session.execute(query).first()
        return result[0] if result else None

    def get_last_user_with_specifi_email(self, email: str) -> UserModel:
        """
        Retrieves the last user registered with the given email.

        Args:
            email (str): Email associated with the user.

        Returns:
            UserModel: Last user registered with the given email, or None if not found.
        """
        query = select(self.model).where(self.model.email == email).order_by(desc(self.model.created))
        result = self.session.execute(query).first()
        return result[0] if result else None

    def get_email_by_user_id(self, user_id: str) -> UserModel:
        """
        Retrieves an EmailModel record associated with the given email.

        Args:
            email (str): Email associated with the record.

        Returns:
            UserModel: User record associated with the given email, or None if not found.
        """
        emails = self.get_by_attributes(user_id=user_id)
        if len(emails) == 0:
            return None
        return emails[0]
