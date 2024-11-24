from typing import TYPE_CHECKING

from context.v1.codes.domain.entities.code import CodeEntity
from context.v1.codes.domain.entities.resend import ResendCodeEntity
from context.v1.codes.domain.steps.create import CreateCodeStep
from context.v1.codes.domain.steps.deactivate import DeactivateCode
from context.v1.codes.domain.steps.find_last import FindLastCode
from context.v1.emails.domain.steps.find import FindEmailStep
from context.v1.login_methods.domain.steps.find import (
    FindLoginMethodStep,
)
from core.settings import email_client, settings
from shared.app.controllers.saga.controller import SagaController
from shared.app.enums.code_type import CodeTypeEnum
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum
from shared.databases.infrastructure.repository import RepositoryInterface
from shared.presentation.templates.email import get_data_for_email_activate_account
from shared.utils.codes import generate_code

if TYPE_CHECKING:
    from context.v1.emails.domain.entities.email import EmailEntity


class ResendCodeUseCase:
    def __init__(
        self,
        code_repository: RepositoryInterface,
        email_repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
    ):
        self.code_repository = code_repository
        self.email_repository = email_repository
        self.login_method_repository = login_method_repository

    def execute(self, payload: ResendCodeEntity):
        controller = SagaController(
            [
                FindEmailStep(email=payload.email, repository=self.email_repository),
                FindLastCode(repository=self.code_repository, type_code=CodeTypeEnum.ACCOUNT_ACTIVATION),
                DeactivateCode(repository=self.code_repository),
                FindLoginMethodStep(
                    find_step_type=FindEmailStep,
                    repository=self.login_method_repository,
                    need_verification=False,
                ),
            ],
        )
        payloads = controller.execute()

        new_code = generate_code(length=settings.LENGHT_CODE_VALIDATE_EMAIL)

        code_entity = CodeEntity(
            code=new_code,
            user_id=payloads[FindEmailStep].user_id,
            entity_id=payloads[FindEmailStep].id,
            entity_type=UserLoginMethodsTypeEnum.EMAIL,
            type=payload.type,
        )

        controller_code = SagaController(
            [
                CreateCodeStep(entity=code_entity, repository=self.code_repository),
            ],
            prev_saga=controller,
        )

        _ = controller_code.execute()

        subject_text, message_text = get_data_for_email_activate_account(
            user_name=payloads[FindEmailStep].email,
            activation_code=new_code,
        )

        email_client.send_email(
            email_subject=payload.email,
            subject_text=subject_text,
            message_text=message_text,
        )

        email_entity: EmailEntity = payloads[FindEmailStep]

        return email_entity
