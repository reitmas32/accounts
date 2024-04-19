import logging

from fastapi import status

from api.v1.users.schemas import (
    RetrieveSingUpEmailEmailSchema,
)
from api.v1.users.schemas.verify import VerifyEmailSchema
from api.v1.users.steps.user import FindUserStep
from core.controllers.saga.controller import SagaController
from core.utils.generic_views import BaseService
from core.utils.responses import (
    create_simple_envelope_response,
)
from models.code import CodeModel

logger = logging.getLogger(__name__)


class LoginEmailService(BaseService):
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
                FindUserStep(user_name=payload.user_name, session=self.session),
            ],
        )

        controller.execute()

        return create_simple_envelope_response(
            data=None,
            message="La cuenta fue activada correctamente",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
