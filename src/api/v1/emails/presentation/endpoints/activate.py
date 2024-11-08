from fastapi import status

from api.v1.emails.presentation.dtos.activate import ActivateEmailDto
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from context.v1.emails.domain.entities.activation import ActivateEmailEntity
from context.v1.emails.domain.usecase.activation import ActivationEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.post(
    "/activate",
    summary="Activate account with code and email",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["Auth API"],
)
async def activate(
    payload: ActivateEmailDto,
):
    logger.info("Activating Account from email")

    entity = ActivateEmailEntity(**payload.model_dump())

    email_repository = EmailRepository()
    code_repository = CodeRepository()

    use_case = ActivationEmailUseCase(
        email_repository=email_repository,
        code_repository=code_repository,
        login_method_repository=LoginMethodRepository(),
    )

    jwt = use_case.execute(payload=entity)

    return EnvelopeResponse(
        data=jwt,
        success=True,
        response_code=status.HTTP_200_OK,
        message="The account has been activated"
    )
