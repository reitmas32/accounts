import logging
from typing import TYPE_CHECKING

from fastapi import status

from api.v1.users.proxies import (
    RepositoryAuthGeneralPlatform,
    RepositoryAuthPhoneNumber,
    RepositoryEmail,
    RepositoryUser,
    RepositoryUserLoginMethod,
)
from api.v1.users.schemas import (
    RetrieveSingUpEmailEmailSchema,
    SignupEmailSchema,
)
from api.v1.users.steps.associate_with_user import AddUserLoginMethodStep
from api.v1.users.steps.code import SendEmailCodeStep
from api.v1.users.steps.email import CreateEmailAuthStep
from api.v1.users.steps.user import CreateUserStep
from api.v1.users.utils import CodeManager
from core.controllers.saga.controller import SagaController
from core.utils.generic_views import BaseService
from core.utils.responses import (
    create_simple_envelope_response,
)
from models.enum import UserLoginMethodsTypeEnum
from models.user import UserModel

if TYPE_CHECKING:
    from models.email import EmailModel

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
    schema = RetrieveSingUpEmailEmailSchema

    def __init__(self, session):
        """
        Initialize the SignUpEmailService.

        Args:
            session: Database session for interacting with the data.
        """
        self.session = session
        self.repository_user = RepositoryUser(session=session)
        self.repository_auth_email = RepositoryEmail(session=session)
        self.repository_phone_number = RepositoryAuthPhoneNumber(session=session)
        self.repository_login_method = RepositoryUserLoginMethod(session=session)
        self.repository_auth_platform = RepositoryAuthGeneralPlatform(session=session)
        self.code_manager = CodeManager(session=session)

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

        user_schema = RetrieveSingUpEmailEmailSchema(
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
