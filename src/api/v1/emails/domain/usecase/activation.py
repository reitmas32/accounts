from datetime import datetime
from typing import TYPE_CHECKING

from api.v1.emails.domain.entities.activation import ActivateEmailEntity
from api.v1.login_methods.domain.steps.create_jwt import CreateJWTStep
from shared.app.controllers.saga.controller import SagaController
from shared.app.enums.code_type import CodeTypeEnum
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum
from shared.app.errors.invalid.code_alredy_use import CodeAlreadyUsedError
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from shared.databases.orms.sqlalchemy.models.code import CodeModel
    from shared.databases.orms.sqlalchemy.models.email import EmailModel
    from shared.databases.orms.sqlalchemy.models.login_methods import LoginMethodModel


class ActivationEmailUseCase:
    def __init__(
        self,
        email_repository: RepositoryInterface,
        code_repository: RepositoryInterface,
        login_method_repository: RepositoryInterface,
    ):
        self.email_repository = email_repository
        self.code_repository = code_repository
        self.login_method_repository = login_method_repository

    def execute(self, payload: ActivateEmailEntity):
        emails: list[EmailModel] = self.email_repository.get_by_attributes(
            filters={"email": payload.email}, limit=1
        )

        if len(emails) == 0:
            raise EntityNotFoundError(resource=f"User with email {payload.email}")

        email = emails[0]

        codes: list[CodeModel] = self.code_repository.get_by_attributes(
            filters={
                "entity_id": str(email.id),
                "entity_type": UserLoginMethodsTypeEnum.EMAIL,
                "type": CodeTypeEnum.ACCOUNT_ACTIVATION,
            },
            limit=1,
        )

        if len(codes) == 0:
            raise EntityNotFoundError(
                resource=f"Code Activation dont found by email {payload.email}"
            )

        code = codes[0]

        if code.used_at is not None:
            raise CodeAlreadyUsedError(code=code.code)

        now = datetime.now().astimezone()

        self.code_repository.update_field_by_id(
            id=str(code.id), field_name="used_at", new_value=now
        )

        login_methods: list[LoginMethodModel] = (
            self.login_method_repository.get_by_attributes(
                filters={
                    "user_id": str(email.user_id),
                    "entity_type": UserLoginMethodsTypeEnum.EMAIL,
                    "entity_id": str(email.id),
                },
            )
        )

        if len(login_methods) == 0:
            raise EntityNotFoundError(
                resource=f"Login Method dont found by email {payload.email}"
            )

        login_method = login_methods[0]

        controller_jwt = SagaController(
            [CreateJWTStep(login_method=login_method)],
        )

        payloads_jwt = controller_jwt.execute()

        return payloads_jwt[CreateJWTStep]
