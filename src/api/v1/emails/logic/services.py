import logging
from typing import TYPE_CHECKING

from fastapi import status

from api.v1.codes.crud.steps import SendEmailCodeStep, VerifyCodeStep
from api.v1.emails.crud.steps import CreateEmailAuthStep
from api.v1.emails.logic.schemas import (
    LoginEmailSchema,
    ResetPasswordConfirmSchema,
    ResetPasswordSchema,
    RetrieveSingUpEmailSchema,
    SignupEmailSchema,
    VerifyEmailSchema,
)
from api.v1.emails.logic.steps import (
    LoginUserStep,
    ResetPasswordConfirmStep,
    ResetPasswordStep,
)
from api.v1.login_methods.steps import AddUserLoginMethodStep
from api.v1.users.crud.steps.associate_with_user import (
    ActivateUserLoginMethodStep,
    FindUserLoginMethodStep,
)
from api.v1.users.crud.steps.user import CreateUserStep, FindUserStep
from core.utils.generic_views import (
    BaseService,
)
from core.utils.responses import (
    create_simple_envelope_response,
)
from shared.app.controllers import SagaController
from shared.app.enums import UserLoginMethodsTypeEnum
from shared.databases.postgres.models.code import CodeModel
from shared.databases.postgres.models.user import UserModel
from shared.utils.email import hide_email

if TYPE_CHECKING:
    from shared.databases.postgres.models.email import EmailModel

logger = logging.getLogger(__name__)


class SignUpEmailService(BaseService):
    """
    Service for email-based user signup.

    This service handles the creation of user accounts using email as the authentication method.

    Args:
        session: Database session for interacting with the data.

    Attributes:
        session: Database session for interacting with the data.
        repository_user: Repository for user data operations.
        repository_auth_email: Repository for email authentication data operations.
        repository_phone_number: Repository for phone number authentication data operations.
        repository_login_method: Repository for user login method data operations.
        repository_auth_platform: Repository for general platform authentication data operations.
        code_manager: Manager for code-related operations.
    """

    model = UserModel
    schema = RetrieveSingUpEmailSchema

    def __init__(self, session):
        """
        Initialize the SignUpEmailService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session

    def create(self, payload: SignupEmailSchema):
        """
        Create a user account using email-based authentication.

        Args:
            payload (SignupEmailSchema): Data payload containing email and password for user signup.

        Returns:
            dict: Envelope response containing user data, message, and status code.
        """
        controller = SagaController(
            [
                CreateUserStep(user=payload, session=self.session),
                CreateEmailAuthStep(
                    email=payload.email,
                    password=payload.password,
                    session=self.session,
                ),
                AddUserLoginMethodStep(
                    type_login=UserLoginMethodsTypeEnum.EMAIL,
                    session=self.session,
                ),
                SendEmailCodeStep(
                    email=payload.email,
                    user_name=payload.user_name,
                    session=self.session,
                ),
            ],
        )
        payloads = controller.execute()

        user: UserModel = payloads[CreateUserStep]
        email_auth: EmailModel = payloads[CreateEmailAuthStep]

        user_schema = RetrieveSingUpEmailSchema(
            id=user.id,
            created=user.created,
            email=email_auth.email,
            updated=user.updated,
            user_name=user.user_name,
        )

        return create_simple_envelope_response(
            data=user_schema.dict(),
            message="User created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )


class LoginEmailService(BaseService):
    model = CodeModel
    schema = RetrieveSingUpEmailSchema

    def __init__(self, session):
        """
        Initialize the SignUpEmailService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session

    def login(self, payload: LoginEmailSchema):
        """
        Create a user account using email-based authentication.

        Args:
            payload (SignupEmailSchema): Data payload containing email and password for user signup.

        Returns:
            dict: Envelope response containing user data, message, and status code.
        """
        controller = SagaController(
            [
                LoginUserStep(
                    user_name=payload.user_name,
                    session=self.session,
                    email=payload.email,
                    password=payload.password,
                ),
            ],
        )

        controller.execute()

        jwt = controller.payloads[LoginUserStep]

        return create_simple_envelope_response(
            data=jwt,
            message="Sesion iniciada con exito",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


class VerifyCodeService(BaseService):
    model = CodeModel
    schema = RetrieveSingUpEmailSchema

    def __init__(self, session):
        """
        Initialize the SignUpEmailService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session

    def verify(self, payload: VerifyEmailSchema):
        """
        Create a user account using email-based authentication.

        Args:
            payload (SignupEmailSchema): Data payload containing email and password for user signup.

        Returns:
            dict: Envelope response containing user data, message, and status code.
        """
        controller = SagaController(
            [
                FindUserStep(user_name=payload.user_name, session=self.session),
                VerifyCodeStep(code=payload.code, session=self.session),
                FindUserLoginMethodStep(
                    type_login=UserLoginMethodsTypeEnum.EMAIL,
                    session=self.session,
                ),
                ActivateUserLoginMethodStep(session=self.session),
            ],
        )

        controller.execute()

        return create_simple_envelope_response(
            data=None,
            message="La cuenta fue activada correctamente",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


class ResetPasswordService(BaseService):
    model = CodeModel
    schema = RetrieveSingUpEmailSchema

    def __init__(self, session):
        """
        Initialize the SignUpEmailService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session

    def reset_password(self, payload: ResetPasswordSchema):
        """
        Create a user account using email-based authentication.

        Args:
            payload (SignupEmailSchema): Data payload containing email and password for user signup.

        Returns:
            dict: Envelope response containing user data, message, and status code.
        """
        controller = SagaController(
            [
                ResetPasswordStep(user_name=payload.user_name, session=self.session),
            ],
        )

        controller.execute()

        email: EmailModel = controller.payloads[ResetPasswordStep]

        email_str = hide_email(email.email)

        return create_simple_envelope_response(
            data=None,
            message=f"Se envio un codigo de verificacion a tu email registrado {email_str}",
            status_code=status.HTTP_200_OK,
            successful=True,
        )


class ResetPasswordConfirmService(BaseService):
    model = CodeModel
    schema = RetrieveSingUpEmailSchema

    def __init__(self, session):
        """
        Initialize the SignUpEmailService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session

    def reset_password(self, payload: ResetPasswordConfirmSchema):
        """
        Create a user account using email-based authentication.

        Args:
            payload (SignupEmailSchema): Data payload containing email and password for user signup.

        Returns:
            dict: Envelope response containing user data, message, and status code.
        """
        controller = SagaController(
            [
                ResetPasswordConfirmStep(
                    user_name=payload.user_name,
                    code=payload.code,
                    password=payload.password,
                    session=self.session,
                ),
                VerifyCodeStep(session=self.session, code=payload.code),
                ActivateUserLoginMethodStep(session=self.session),
            ],
        )

        controller.execute()

        user: UserModel = controller.payloads[ResetPasswordConfirmStep]

        return create_simple_envelope_response(
            data=None,
            message=f"Se activo la nueva contraseña para {user.user_name}",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
