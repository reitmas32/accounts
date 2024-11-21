from fastapi import status

from api.v1.emails.presentation.dtos.activate import ActivateEmailDto
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from context.v1.emails.domain.entities.activation import ActivateEmailEntity
from context.v1.emails.domain.usecase.activation import ActivationEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_operations as router


@router.post(
    "/activate",
    summary="Activate account with code and email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
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
        refresh_token_repository=RefreshTokenRepository(),
    )

    jwt, refresh_token = use_case.execute(payload=entity)

    return ResponseEntity(
        data={
            "jwt": jwt,
            "refresh_token": refresh_token
        },
        code=StatusCodes.HTTP_200_OK,
    )
