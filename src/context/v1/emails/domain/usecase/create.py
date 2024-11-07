import random
import string
from datetime import datetime

from context.v1.codes.domain.entities.code import CodeEntity
from context.v1.codes.domain.steps.create import CreateCodeStep
from context.v1.emails.domain.entities.email import EmailEntity
from context.v1.emails.domain.entities.signup import SignupEmailEntity
from context.v1.emails.domain.steps.create import CreateEmailStep
from context.v1.login_methods.domain.steps.create import (
    CreateLoginMethodEmailStep,
)
from context.v1.users.domain.steps.create import CreateUserByUserNameStep
from core.settings import email_client, settings
from shared.app.controllers.saga.controller import SagaController
from shared.app.enums.code_type import CodeTypeEnum
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum
from shared.databases.infrastructure.repository import RepositoryInterface
from shared.presentation.templates.email import get_data_for_email_activate_account


def generate_code(length):
    """
    Generate a verification code.

    Args:
        length (int): Length of the verification code.

    Returns:
        str: Generated verification code.
    """
    return "".join(random.choices(string.digits, k=length))  # noqa: S311


class CreateEmailUseCase:
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: EmailEntity):
        return self.repository.add(**payload.model_dump())


class SignUpWithEmailUseCase:
    def __init__(
        self,
        user_repository: RepositoryInterface,
        email_repository: RepositoryInterface,
        code_repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
        user_name: str | None = None,
    ):
        self.user_repository = user_repository
        self.email_repository = email_repository
        self.code_repository = code_repository
        self.login_method_repository = login_method_repository
        self.user_name = user_name

    def execute(self, payload: SignupEmailEntity):

        email_entity = EmailEntity(**payload.model_dump())

        controller = SagaController(
            [
                CreateUserByUserNameStep(
                    user_name=payload.user_name, repository=self.user_repository
                ),
                CreateEmailStep(entity=email_entity, repository=self.email_repository),
                CreateLoginMethodEmailStep(repository=self.login_method_repository),
            ],
        )

        payloads = controller.execute()

        new_code = generate_code(length=settings.LENGHT_CODE_VALIDATE_EMAIL)

        code_entity = CodeEntity(
            code=new_code,
            user_id=payloads[CreateUserByUserNameStep].id,
            entity_id=payloads[CreateEmailStep].id,
            entity_type=UserLoginMethodsTypeEnum.EMAIL,
            type=CodeTypeEnum.SIGN_UP,
            used_at=datetime.now().astimezone(),
        )

        controller_code = SagaController(
            [
                CreateCodeStep(entity=code_entity, repository=self.code_repository),
            ],
            prev_saga=controller,
        )

        _ = controller_code.execute()

        subject_text, message_text = get_data_for_email_activate_account(
            user_name=payloads[CreateUserByUserNameStep].user_name, activation_code=new_code
        )

        email_client.send_email(
            email_subject=payload.email,
            subject_text=subject_text,
            message_text=message_text,
        )

        email_entity: EmailEntity = payloads[CreateEmailStep]

        return email_entity

