from uuid import UUID

from fastapi import status

from api.v1.users.proxies import RepositoryUser
from api.v1.users.schemas import RetrieveUserSchema
from core.utils.responses import create_envelope_response


class RetrieveUserService:
    """
    Service for retrieving user information.

    This service provides methods for retrieving user data, either by ID or all users.

    Args:
        session: Database session for interacting with the data.

    Attributes:
        session: Database session for interacting with the data.
        repository_user: Repository for user data operations.
    """

    def __init__(self, session):
        """
        Initialize the RetrieveUserService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session
        self.repository_user = RepositoryUser(session=session)

    def retrieve_by_id(self, id: UUID):
        """
        Retrieve user information by ID.

        Args:
            id (UUID): ID of the user to retrieve.

        Returns:
            dict: Envelope response containing user data, count, message, and status code.
        """
        user = self.repository_user.get_by_id(id=id)
        data = None
        count = 0
        if user:
            data = RetrieveUserSchema(**user.as_dict())
            count = 1
        return create_envelope_response(
            data=data,
            count=count,
            message="User Retrieve",
            status_code=status.HTTP_200_OK,
            successful=True,
        )

    def retrieve_all(self):
        """
        Retrieve information for all users.

        Returns:
            dict: Envelope response containing user data, count, message, and status code.
        """
        users = self.repository_user.get_all()
        count = 0
        data = [user.as_dict() for user in users]
        count = len(data)
        return create_envelope_response(
            data=data,
            count=count,
            message="User List",
            status_code=status.HTTP_200_OK,
            successful=True,
        )

