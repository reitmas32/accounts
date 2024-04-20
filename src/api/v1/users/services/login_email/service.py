import logging

from fastapi import status

from api.v1.users.schemas import (
    RetrieveSingUpEmailEmailSchema,
)
from api.v1.users.services.login_email.schema import LoginEmailSchema
from api.v1.users.services.login_email.steps import (
    AccountIsVerifiedStep,
    ActivateLoginStep,
    CreateJWTStep,
    FindEmailOfUserByEmailOrUserNameStep,
    PasswordVerifyStep,
)
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
        self.session = session

    def login(self, payload: LoginEmailSchema):
        logger.info(payload)

        controller = SagaController(
            [
                FindEmailOfUserByEmailOrUserNameStep(
                    user_name=payload.user_name, email=payload.email, session=self.session
                ),
                PasswordVerifyStep(session=self.session, password=payload.password),
                AccountIsVerifiedStep(session=self.session),
                CreateJWTStep(session=self.session),
                ActivateLoginStep(session=self.session),
            ],
        )

        result = controller.execute()

        jwt = result[CreateJWTStep]

        return create_simple_envelope_response(
            data={"JWT": jwt},
            message="Se inicio secion correctamente",
            status_code=status.HTTP_200_OK,
            successful=True,
        )
