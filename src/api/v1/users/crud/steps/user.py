from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from api.v1.emails.crud.proxies import RepositoryEmail
from api.v1.emails.logic.schemas import SignupEmailSchema
from api.v1.login_methods.proxies import LoginMethodsProxy, RepositoryUserLoginMethod
from api.v1.users.crud.proxies import RepositoryUser
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import (
    DontFindResourceException,
    PasswordNoneException,
    PasswordNotValidException,
    UserNameAndEmailIsEmptyException,
    UserNameUniqueException,
)
from core.utils.password import PasswordManager

if TYPE_CHECKING:
    from models import UserModel


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

    def __init__(
        self, user: SignupEmailSchema, session: Session
    ):  # TODO: Change SignupEmailSchema to UserSchema
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


class LoginUserStep(StepSAGA):
    def __init__(
        self,
        session: Session,
        user_name: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_name = user_name
        self.email = email
        self.password = password
        self.password_manager = PasswordManager()
        self.repository_user = RepositoryUser(session=session)
        self.repository_email = RepositoryEmail(session=session)
        self.repository_login_method = RepositoryUserLoginMethod(session=session)

    def verify(self):
        if self.user_name is None and self.email is None:
            raise UserNameAndEmailIsEmptyException

        if self.password is None:
            raise PasswordNoneException

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        user = self.repository_user.get_user(user_name=self.user_name)
        if user is None:
            raise DontFindResourceException(resource=self.user_name)

        email = self.repository_email.get_email_by_user_id(user_id=user.id)
        if email is None:
            raise DontFindResourceException(resource=self.email)

        if not self.password_manager.verify_password(self.password, email.password):
            raise PasswordNotValidException

        self.login_method = self.repository_login_method.get_by_attributes(
            user_id=user.id, entity_id=email.id, verify=True
        )
        if self.login_method is None or len(self.login_method) == 0:
            raise DontFindResourceException(
                message="The login email is dont exist by this user", resource=""
            )

        self.repository_login_method.update_field_by_id(
            id=self.login_method.id, field_name="active", new_value=True
        )

        return user

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        self.repository_login_method.update_field_by_id(
            id=self.login_method.id, field_name="active", new_value=False
        )
