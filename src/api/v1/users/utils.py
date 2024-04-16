import random
import string
from datetime import timedelta

from sqlalchemy.orm import Session

from api.v1.users.proxies import RepositoryCode
from api.v1.users.resources import (
    get_data_for_email_activate_account,
    get_data_for_email_two_factor,
)
from core.settings import settings
from core.utils.email import (
    SendEmailAbstract,
    get_current_manager_email_to_app_standard,
)
from core.utils.responses import get_current_date_time_to_app_standard
from models.code import CodeTypeEnum


class CodeManager:
    """
    Manager class for handling code-related operations.

    This manager is responsible for generating, creating, sending, and validating codes used in the authentication process.

    Args:
        session: Database session for interacting with the data.

    Attributes:
        repository_code: Repository for code data operations.
        manager_email: Email manager for sending emails.
    """

    def __init__(self, session: Session):
        """
        Initialize the CodeManager.

        Args:
            session: Database session for interacting with the data.
        """
        self.repository_code = RepositoryCode(session=session)
        self.manager_email: SendEmailAbstract = get_current_manager_email_to_app_standard()

    def generate_code(self, length):
        """
        Generate a random code.

        Args:
            length (int): Length of the generated code.

        Returns:
            str: Generated code.
        """
        return "".join(random.choices(string.digits, k=length))  # noqa: S311

    def create_and_send_code(self, email, user_name, code_type: CodeTypeEnum):
        """
        Generate, create, and send a code via email.

        Args:
            email (str): Email address to send the code to.
            user_name (str): Username associated with the email address.
            code_type (CodeTypeEnum): Type of code to generate and send.
        """
        code_length = settings.LENGHT_CODE_VALIDATE_EMAIL
        if code_type.value == CodeTypeEnum.TWO_FACTOR.value:
            code_length = settings.LENGHT_CODE_2FA
        new_code = self.generate_code(length=code_length)
        if code_type.value == CodeTypeEnum.TWO_FACTOR.value:
            subject_text, message_text = get_data_for_email_two_factor(user_name=user_name, two_factor_code=new_code)
        else:
            subject_text, message_text = get_data_for_email_activate_account(
                user_name=user_name, activation_code=new_code
            )
        self.repository_code.add(code=new_code, email=email, type=code_type)
        self.manager_email.send_email(
            email_subject=email,
            subject_text=subject_text,
            message_text=message_text,
        )

    def validate_code(self, email, code, code_type: CodeTypeEnum):
        """
        Validate a code.

        Args:
            email (str): Email address associated with the code.
            code (str): Code to validate.
            code_type (CodeTypeEnum): Type of code to validate.

        Returns:
            bool: True if the code is valid, False otherwise.
        """
        time_seconds_expire = settings.TIME_SECONDS_EXPIRE_CODE_2FA
        if code_type.value == CodeTypeEnum.ACCOUNT_ACTIVATION.value:
            time_seconds_expire = settings.TIME_SECONDS_EXPIRE_CODE_VALIDATE_EMAIL
        current_time = get_current_date_time_to_app_standard()
        min_created = current_time - timedelta(seconds=time_seconds_expire)

        code_entry = self.repository_code.get_code(email=email, code=code, min_created=min_created)

        if code_entry:
            self.repository_code.update_field_by_id(id=code_entry.id, field_name="used_at", new_value=current_time)
            return True
        return False
