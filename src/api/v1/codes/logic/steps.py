import random
import string

from sqlalchemy.orm import Session

from api.v1.users.proxies import RepositoryCode
from api.v1.users.resources import (
    get_data_for_email_activate_account,
)
from core.controllers.saga.controller import StepSAGA
from core.settings import settings
from core.utils.email import (
    SendEmailAbstract,
    get_current_manager_email_to_app_standard,
)
from models.enum import CodeTypeEnum
from models.login_methods import LoginMethodModel


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
        self.manager_email: SendEmailAbstract = get_current_manager_email_to_app_standard()

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

        self.manager_email.send_email(
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
