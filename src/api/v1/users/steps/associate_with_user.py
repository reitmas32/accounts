from datetime import datetime, timezone

from sqlalchemy.orm import Session

from api.v1.users.proxies import (
    RepositoryUserLoginMethod,
)
from api.v1.users.proxies.code import RepositoryCode
from api.v1.users.steps.code import VerifyCodeStep
from api.v1.users.steps.user import FindUserStep
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import DontFindResourceException
from models.email import EmailModel
from models.code import CodeModel
from models.enum import UserLoginMethodsTypeEnum
from models.user import UserModel
from models.user_login_methods import UserLoginMethodModel


class AddUserLoginMethodStep(StepSAGA):
    """
    Step in the SAGA process for adding a user login method.

    This step handles the addition of a user login method, such as email or phone number, during the signup process.

    Args:
        type_login (UserLoginMethodsTypeEnum): Type of login method to add.
        session: Database session for interacting with the data.

    Attributes:
        repository: Repository for user login method data operations.
        type_login (UserLoginMethodsTypeEnum): Type of login method to add.
        user_login_method: User login method object created during the step.
    """

    def __init__(
        self,
        type_login: UserLoginMethodsTypeEnum,
        session: Session,
    ):
        """
        Initialize the AddUserLoginMethodStep.

        Args:
            type_login (UserLoginMethodsTypeEnum): Type of login method to add.
            session: Database session for interacting with the data.
        """
        self.repository = RepositoryUserLoginMethod(session=session)
        self.type_login: UserLoginMethodsTypeEnum = type_login
        self.user_login_method = None

    def __call__(self, payload: EmailModel, all_payloads: dict | None = None):
        """
        Execute the step, adding a user login method.

        Args:
            payload (EmailModel): Data payload containing authentication email model.

        Returns:
            UserLoginMethodModel: User login method object created during the step.
        """
        self.user_login_method = self.repository.add(
            user_id=payload.user_id,
            entity_id=payload.id,
            entity_type=self.type_login,
            active=False,
        )

        return self.user_login_method

    def rollback(self):
        """
        Rollback the step, deleting the user login method if it was created.
        """
        if self.user_login_method is not None:
            self.repository.delete_by_id(self.user_login_method.id)


class FindUserLoginMethodStep(StepSAGA):
    def __init__(
        self,
        type_login: UserLoginMethodsTypeEnum,
        session: Session,
    ):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.repository = RepositoryUserLoginMethod(session=session)
        self.type_login: UserLoginMethodsTypeEnum = type_login

    def __call__(self, payload: UserModel | None = None, all_payloads: dict | None = None):
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        user: UserModel = all_payloads[FindUserStep]
        login_method = self.repository.get_by_attributes(
            user_id=user.id.__str__(), entity_type=self.type_login, active=False
        )
        if login_method is None:
            raise DontFindResourceException(resource="login_method")

        return login_method[0]

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class ActivateUserLoginMethodStep(StepSAGA):
    """
    Step in the SAGA process for adding a user login method.

    This step handles the addition of a user login method, such as email or phone number, during the signup process.

    Args:
        type_login (UserLoginMethodsTypeEnum): Type of login method to add.
        session: Database session for interacting with the data.

    Attributes:
        repository: Repository for user login method data operations.
        type_login (UserLoginMethodsTypeEnum): Type of login method to add.
        user_login_method: User login method object created during the step.
    """

    def __init__(
        self,
        session: Session,
    ):
        """
        Initialize the AddUserLoginMethodStep.

        Args:
            type_login (UserLoginMethodsTypeEnum): Type of login method to add.
            session: Database session for interacting with the data.
        """

        self.repository_auth = RepositoryUserLoginMethod(session=session)
        self.repository_code = RepositoryCode(session=session)

    def __call__(self, payload: UserLoginMethodModel, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, adding a user login method.

        Args:
            payload (EmailModel): Data payload containing authentication email model.

        Returns:
            UserLoginMethodModel: User login method object created during the step.
        """
        now = datetime.now(tz=timezone.utc)
        self.auth_id = payload.id
        code: CodeModel = all_payloads[VerifyCodeStep]
        self.repository_auth.update_field_by_id(id=self.auth_id, field_name="active", new_value=True)
        self.repository_code.update_field_by_id(id=code.id.__str__(), field_name="used_at", new_value=now)

        return True

    def rollback(self):
        """
        Rollback the step, deleting the user login method if it was created.
        """
        self.repository_auth.update_field_by_id(id=self.auth_id, field_name="active", new_value=False)
        self.repository_code.update_field_by_id(id=self.code_id, field_name="used_at", new_value=None)
