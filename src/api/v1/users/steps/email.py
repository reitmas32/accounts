import re
from datetime import datetime

from sqlalchemy.orm import Session

from api.v1.users.proxies import RepositoryEmail
from api.v1.users.proxies.code import RepositoryCode
from core.controllers.saga.controller import StepSAGA
from core.utils.exceptions import (
    DontFindResourceException,
    EmailUniqueException,
    PasswordNoneException,
    PasswordNotValidException,
)
from core.utils.password import PasswordManager
from models import UserModel
from models.code import CodeModel


class CreateEmailAuthStep(StepSAGA):
    """
    Step in the SAGA process for creating email authentication.

    This step handles the creation of email authentication during the signup process.

    Args:
        email (str): Email address for authentication.
        password (str): Password for the email authentication.
        session: Database session for interacting with the data.

    Attributes:
        email (str): Email address for authentication.
        password (str): Password for the email authentication.
        auth_email_created: Email authentication object created during the step.
        repository: Repository for email authentication data operations.
    """

    def __init__(
        self,
        email: str,
        password: str,
        session: Session,
    ):
        """
        Initialize the CreateEmailAuthStep.

        Args:
            email (str): Email address for authentication.
            password (str): Password for the email authentication.
            session: Database session for interacting with the data.
        """
        self.email = email
        self.password = password
        self.auth_email_created = None
        self.repository = RepositoryEmail(session=session)

    @staticmethod
    def validate_password(password: str):
        """
        Validate the password format.

        Args:
            password (str): Password to validate.

        Raises:
            PasswordNoneException: If password is None.
            PasswordNotValidException: If password does not meet the required pattern.
        """
        if password is None:
            raise PasswordNoneException

        return
        # Regular expression to validate the password
        regex = (
            r"^(?=.*\d)(?=.*[&%$*?¿¡!])(?=.*[A-Z])(?=.*[a-z])[A-Za-z\d&%$*?¿¡!]{8,}$"
        )

        # Check if the password matches the pattern
        if not re.match(regex, password):
            raise PasswordNotValidException

    def __call__(self, payload: UserModel, all_payloads: dict | None = None):
        """
        Execute the step, creating email authentication.

        Args:
            payload (UserModel): Data payload containing user model.

        Returns:
            EmailModel: Email authentication object created during the step.
        """
        CreateEmailAuthStep.validate_password(self.password)

        existing_email = self.repository.get_auth_email(email=self.email)

        if existing_email is not None:
            raise EmailUniqueException(email=self.email)

        self.auth_email_created = self.repository.add(
            user_id=payload.id,
            email=self.email,
            password=PasswordManager.hash_password(password=self.password),
        )

        return self.auth_email_created

    def rollback(self):
        """
        Rollback the step, deleting the email authentication if it was created.
        """
        if self.auth_email_created is not None:
            self.repository.delete_by_id(self.auth_email_created.id)

class FindEmailStep(StepSAGA):
    def __init__(self, email: str ,session: Session):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_created = None
        self.email = email
        self.repository = RepositoryEmail(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        email = self.repository.get_auth_email(email=self.email)
        if email is None:
            raise DontFindResourceException(resource=self.email)

        return email

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class ActivateEmailStep(StepSAGA):
    def __init__(self, code: str ,session: Session):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_created = None
        self.code = code
        self.repository_email = RepositoryEmail(session=session)
        self.repository_code = RepositoryCode(session=session)


    def __call__(self, payload: CodeModel | None = None, all_payloads: dict | None = None):
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        self.payload = payload
        datetime_now = datetime.now().astimezone()
        self.repository_email.update_field_by_id(id=payload.entity_id, field_name="active", new_value=True)
        self.repository_code.update_field_by_id(id=payload.id, field_name="used_at", new_value=datetime_now)
        return self.repository.get_code(code=self.code)

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """ #NOTE: si hay un error al usar el codigo deberiamos marcarcomo usado el codigo??
        self.repository_email.update_field_by_id(id=self.payload.entity_id, field_name="active", new_value=False)
        self.repository_code.update_field_by_id(id=self.payload.id, field_name="used_at", new_value=None)

