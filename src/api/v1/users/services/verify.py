import logging

from fastapi import status

from api.v1.users.schemas import (
    RetrieveSingUpEmailEmailSchema,
    SignupEmailSchema,
)
from api.v1.users.schemas.user import UserSchema
from api.v1.users.schemas.verify import VerifyEmailSchema
from api.v1.users.steps.associate_with_user import (
    ActivateUserLoginMethodStep,
    AddUserLoginMethodStep,
    FindUserLoginMethodStep,
)
from api.v1.users.steps.code import SendEmailCodeStep, VerifyCodeStep
from api.v1.users.steps.email import CreateEmailAuthStep, FindEmailStep
from api.v1.users.steps.user import CreateUserStep, FindUserStep
from api.v1.users.utils import CodeManager
from core.controllers.saga.controller import SagaController
from core.utils.generic_views import BaseService
from core.utils.responses import (
    create_simple_envelope_response,
)
from models.code import CodeModel
from models.enum import UserLoginMethodsTypeEnum
from models.user import UserModel

logger = logging.getLogger(__name__)


class VerifyCodeService(BaseService):
    model = CodeModel
    schema = RetrieveSingUpEmailEmailSchema

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
            data="user_schema.dict()",
            message="User created successfully",
            status_code=status.HTTP_201_CREATED,
            successful=True,
        )
