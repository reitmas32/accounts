import random
import string
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pytz import timezone as tz
from sqlalchemy.orm import Session

from api.v1.codes.crud.services import RepositoryCode
from api.v1.users.crud.resources import (
    get_data_for_email_activate_account,
)
from core.settings import email_client, settings
from shared.app.controllers.saga.controller import StepSAGA
from shared.app.enums import CodeTypeEnum
from shared.app.errors.invalid import (
    CodeAlreadyUsedError,
    CodeExpiredError,
    CodeInvalidError,
)
from shared.databases.errors import EntityNotFoundError
from shared.databases.postgres.models.login_methods import LoginMethodModel
from shared.databases.postgres.models.user import UserModel

if TYPE_CHECKING:
    from shared.app.repositories.email.send import SendEmailRepository


class SendEmailCodeStep(StepSAGA):
    """
    Step in the SAGA process for sending an email verification code.

    This step handles the generation and sending of an email verification code during the signup process.

    Args:
        email (str): Email address to send the verification code to.
        user_name (str): Username associated with the email address.
        session: Database session for interacting with the data.

    Attributes:
        email (str): Email address to send the verification code to.
        user_name (str): Username associated with the email address.
        code_created: Code object created during the step.
        repository: Repository for code data operations.
        manager_email: Email manager for sending the verification email.
    """

    def __init__(self, email: str, user_name: str, session: Session):
        """
        Initialize the SendEmailCodeStep.

        Args:
            email (str): Email address to send the verification code to.
            user_name (str): Username associated with the email address.
            session: Database session for interacting with the data.
        """
        self.email = email
        self.user_name = user_name
        self.code_created = None
        self.repository = RepositoryCode(session=session)
        self.email_client: SendEmailRepository = email_client

    def generate_code(self, length):
        """
        Generate a verification code.

        Args:
            length (int): Length of the verification code.

        Returns:
            str: Generated verification code.
        """
        return "".join(random.choices(string.digits, k=length))  # noqa: S311

    def __call__(self, payload: LoginMethodModel, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, generating and sending the verification code.

        Args:
            payload (LoginMethodModel): Data payload containing user login method model.

        Returns:
            CodeModel: Code object created during the step.
        """
        code_length = settings.LENGHT_CODE_VALIDATE_EMAIL

        new_code = self.generate_code(length=code_length)

        subject_text, message_text = get_data_for_email_activate_account(
            user_name=self.user_name, activation_code=new_code
        )
        self.code_created = self.repository.add(
            code=new_code,
            entity_id=payload.entity_id,
            entity_type=payload.entity_type,
            type=CodeTypeEnum.ACCOUNT_ACTIVATION,
            user_id=payload.user_id,
        )

        self.email_client.send_email(
            email_subject=self.email,
            subject_text=subject_text,
            message_text=message_text,
        )

        return self.code_created

    def rollback(self):
        """
        Rollback the step, deleting the verification code if it was created.
        """
        if self.code_created is not None:
            self.repository.delete_by_id(self.code_created.id)


class FindCodeStep(StepSAGA):
    def __init__(self, code: str, session: Session):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.code = code
        self.repository = RepositoryCode(session=session)

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        code = self.repository.get_code(code=self.code)
        if code is None:
            raise EntityNotFoundError(resource=self.email)

        return code

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class VerifyCodeStep(StepSAGA):
    def __init__(self, code: str, session: Session):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.code = code
        self.repository = RepositoryCode(session=session)

    def __call__(
        self,
        payload: UserModel | None = None,
        all_payloads: dict | None = None,  # noqa: ARG002
    ):
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        now = datetime.now(timezone.utc)

        self.code_model = self.repository.get_code_by_user_id(code=self.code, user_id=payload.id)
        if self.code_model is None:
            raise CodeInvalidError(code=self.code)
        if self.code_model.used_at is not None:
            raise CodeAlreadyUsedError(user_name=payload.user_name, code=self.code)

        code_date: datetime = self.code_model.created.replace(tzinfo=tz("UTC"))

        self.repository.update_field_by_id(id=self.code_model.id, field_name="used_at", new_value=now)

        timedelta_code = now - code_date
        if int(timedelta_code.total_seconds()) > settings.TIME_SECONDS_EXPIRE_VERIFICATION_CODE:
            raise CodeExpiredError(code=self.code)
        return self.code_model

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        if self.code_created is not None:
            self.repository.delete_by_id(self.code_model.id)
