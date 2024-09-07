from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from api.v1.emails.logic.schemas import SignupEmailSchema
from api.v1.users.crud.proxies import RepositoryUser
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import (
    DontFindResourceException,
    UserNameUniqueException,
)

if TYPE_CHECKING:
    from shared.databases.postgres.models import UserModel


class CreateUserStep(StepSAGA):
    """
    Step in the SAGA process for creating a user.

    This step handles the creation of a user account during the signup process.

    Args:
        user (SignupEmailSchema): Data schema containing user signup information.
        session: Database session for interacting with the data.

    Attributes:
        user_created: User object created during the step.
        user (SignupEmailSchema): Data schema containing user signup information.
        repository: Repository for user data operations.
    """

    def __init__(self, user: SignupEmailSchema, session: Session):  # TODO: Change SignupEmailSchema to UserSchema
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_created = None
        self.user = user
        self.repository = RepositoryUser(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        existing_user_name = self.repository.get_user(user_name=self.user.user_name)
        if existing_user_name is not None:
            raise UserNameUniqueException(user_name=self.user.user_name)

        self.user_created: UserModel = self.repository.add(
            user_name=self.user.user_name,
            birthday=self.user.birthday,
            name=self.user.name,
        )

        if self.user_created is None:
            raise UserNameUniqueException(user_name=self.user.user_name)

        return self.user_created

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        if self.user_created is not None:
            self.repository.delete_by_id(self.user_created.id)


class FindUserStep(StepSAGA):
    def __init__(self, user_name: str, session: Session):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_name = user_name
        self.repository = RepositoryUser(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        user = self.repository.get_user(user_name=self.user_name)
        if user is None:
            raise DontFindResourceException(resource=self.user_name)

        return user

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
