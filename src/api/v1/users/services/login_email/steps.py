from typing import TYPE_CHECKING

from sqlalchemy.orm import Session

from api.v1.users.proxies import RepositoryUser
from api.v1.users.proxies.auth_email import RepositoryEmail
from api.v1.users.proxies.user_login_method import RepositoryUserLoginMethod
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import (
    AccountUnverifiedException,
    DontFindResourceException,
    PasswordNotValidException,
)
from core.utils.jwt import JWTHandler, TokenDataSchema
from core.utils.password import PasswordManager
from models.email import EmailModel

if TYPE_CHECKING:
    from models.login_methods import UserLoginMethodModel


class FindEmailOfUserByEmailOrUserNameStep(StepSAGA):
    def __init__(
        self,
        session: Session,
        user_name: str | None = None,
        email: str | None = None,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_name = user_name
        self.email = email
        self.repository_email = RepositoryEmail(session=session)
        self.repository_user = RepositoryUser(session=session)

    def get_email_of_user(self):
        user_obj = None
        email_obj = None

        if self.user_name is not None:
            user_obj = self.get_user_by_name(self.user_name)
            email_obj = self.repository_email.get_email_by_user_id(str(user_obj.id))
            if email_obj is None:
                raise DontFindResourceException(message="Email dont find of user_name:", resource=self.user_name)
        elif self.email is not None:
            email_obj = self.get_email(self.email)
        else:
            raise DontFindResourceException(message="User and email not provided")

        return email_obj

    def get_user_by_name(self, user_name):
        user = self.repository_user.get_user(user_name=user_name)
        if user is None:
            raise DontFindResourceException(message="User dont find with user_name", resource=user_name)
        return user

    def get_email(self, email_str):
        email = self.repository_email.get_auth_email(email=email_str)
        if email is None:
            raise DontFindResourceException(message="User dont find with email", resource=email_str)
        return email

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        return self.get_email_of_user()

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class PasswordVerifyStep(StepSAGA):
    def __init__(
        self,
        password: str,
        session: Session,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.password = password
        self.repository_email = RepositoryEmail(session=session)

    def __call__(
        self,
        payload: EmailModel | None = None,
        all_payloads: dict | None = None,  # noqa: ARG002
    ):
        password_manager = PasswordManager()
        password_is_valid = password_manager.verify_password(
            plain_password=self.password, hashed_password=payload.password
        )

        if not password_is_valid:
            raise PasswordNotValidException(message="La contraseña no es valida")

        return password_is_valid

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class AccountIsVerifiedStep(StepSAGA):
    def __init__(
        self,
        session: Session,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.repository_user_login = RepositoryUserLoginMethod(session=session)

    def __call__(self, payload: EmailModel | None = None, all_payloads: dict | None = None):
        email: EmailModel = all_payloads[FindEmailOfUserByEmailOrUserNameStep]
        login = self.repository_user_login.get_by_attributes(user_id=email.user_id)

        if len(login) == 0:
            raise DontFindResourceException(message="User dont find with email login method", resource=payload.email)

        login: UserLoginMethodModel = login[0]
        if login.verify is False:
            raise AccountUnverifiedException

        return login

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class CreateJWTStep(StepSAGA):
    def __init__(
        self,
        session: Session,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.repository_email = RepositoryEmail(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        email: EmailModel = all_payloads[FindEmailOfUserByEmailOrUserNameStep]
        return JWTHandler.create_token(data=TokenDataSchema(user_id=str(email.user_id)))

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class ActivateLoginStep(StepSAGA):
    def __init__(
        self,
        session: Session,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.repository_email = RepositoryEmail(session=session)

    def __call__(
        self,
        payload: EmailModel | None = None,
        all_payloads: dict | None = None,
    ):
        pass

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
