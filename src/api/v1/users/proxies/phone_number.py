from sqlalchemy import select

from core.utils.repository_base import RepositoryBase
from models.phone_number import PhoneNumberModel


class RepositoryAuthPhoneNumber(RepositoryBase):
    """
    Repository for operations related to phone number authentication.

    This repository provides methods for performing queries and operations on the PhoneNumberModel table.

    Args:
        RepositoryBase: Base class for repositories.

    Attributes:
        model: Model associated with the PhoneNumberModel table.

    Methods:
        exists_phone_number: Checks if a record with the given phone number exists.
    """

    model: PhoneNumberModel = PhoneNumberModel

    def exists_phone_number(self, phone_number: str) -> bool:
        """
        Checks if a record with the given phone number exists.

        Args:
            phone_number (str): Phone number to check.

        Returns:
            bool: True if a record with the given phone number exists, False otherwise.
        """
        query = select(self.model).where(self.model.phone_number == phone_number)
        result = self.session.execute(query).first()
        return result is not None
