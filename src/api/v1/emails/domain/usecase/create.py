import random
import string
from typing import TYPE_CHECKING

from api.v1.emails.domain.entities.email import EmailEntity
from api.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from core.settings import email_client, settings
from shared.app.enums.code_type import CodeTypeEnum
from shared.app.enums.user_login_methods import UserLoginMethodsTypeEnum
from shared.app.errors.uniques.email_unique import EmailUniqueError
from shared.app.errors.uniques.user_name_unique import UserNameUniqueError
from shared.databases.infrastructure.repository import RepositoryInterface
from shared.presentation.templates.email import get_data_for_email_activate_account

if TYPE_CHECKING:
    from shared.databases.orms.sqlalchemy.models.code import CodeModel
    from shared.databases.orms.sqlalchemy.models.email import EmailModel
    from shared.databases.orms.sqlalchemy.models.login_methods import LoginMethodModel
    from shared.databases.orms.sqlalchemy.models.user import UserModel


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

    def execute(self, payload: EmailEntity):
        self.user_model: UserModel = None
        self.email_model: EmailModel = None
        self.code: CodeModel = None
        self.login_method: LoginMethodModel = None
        try:
            user_entity = self.user_repository.get_by_attributes(
                filters={"user_name": self.user_name}
            )

            if len(user_entity) != 0:
                raise UserNameUniqueError(user_name=self.user_name)  # noqa: TRY301

            email_entity = self.email_repository.get_by_attributes(
                filters={"email": payload.email}
            )

            if len(email_entity) != 0:
                raise EmailUniqueError(email=payload.email)  # noqa: TRY301

            self.user_model: UserModel = self.user_repository.add(
                user_name=self.user_name
            )

            payload.user_id = self.user_model.id

            self.email_model = self.email_repository.add(**payload.model_dump())

            new_code = generate_code(length=settings.LENGHT_CODE_VALIDATE_EMAIL)

            self.code: CodeModel = self.code_repository.add(
                code=new_code,
                user_id=self.user_model.id,
                entity_id=self.email_model.id,
                entity_type=UserLoginMethodsTypeEnum.EMAIL,
                type=CodeTypeEnum.ACCOUNT_ACTIVATION,
            )
            subject_text, message_text = get_data_for_email_activate_account(
                user_name=self.user_model.user_name, activation_code=new_code
            )

            email_client.send_email(
                email_subject=self.email_model.email,
                subject_text=subject_text,
                message_text=message_text,
            )

            login_method = LoginMethodEntity(
                user_id=self.user_model.id,
                entity_id=self.email_model.id,
                entity_type=UserLoginMethodsTypeEnum.EMAIL,
                active=True,
                verify=True,
            )
            self.login_method = self.login_method_repository.add(**login_method.model_dump())

            return self.email_model  # noqa: TRY300
        except Exception as e:
            self.rollback()
            raise e  # noqa: TRY201

    def rollback(self):
        # Eliminar el user y el email si hubo error en el proceso
        if self.code:
            self.code_repository.delete_by_id(self.code.id)
        if self.email_model:
            self.email_repository.delete_by_id(self.email_model.id)
        if self.user_model:
            self.user_repository.delete_by_id(self.user_model.id)
        if self.login_method:
            self.repository.delete_by_id(self.login_method.id)
