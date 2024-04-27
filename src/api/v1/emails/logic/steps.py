from sqlalchemy.orm import Session

from api.v1.emails.crud.proxies import RepositoryEmail
from api.v1.login_methods.proxies import RepositoryUserLoginMethod
from api.v1.users.crud.proxies import RepositoryUser
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import (
    DontFindResourceException,
    PasswordNoneException,
    PasswordNotValidException,
    UserNameAndEmailIsEmptyException,
)
from core.utils.jwt import JWTHandler, TokenDataSchema
from core.utils.password import PasswordManager


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
            id=self.login_method[0].id, field_name="active", new_value=True
        )

        return JWTHandler.create_token(TokenDataSchema(user_id=user.id.__str__()))

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        self.repository_login_method.update_field_by_id(
            id=self.login_method[0].id, field_name="active", new_value=False
        )
