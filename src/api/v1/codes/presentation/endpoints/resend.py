from typing import TYPE_CHECKING

from fastapi import Request, status

from api.v1.codes.presentation.dtos.resend import ResendCodeDto
from api.v1.emails.presentation.schemas.signup import SignupEmailSchema
from context.v1.codes.domain.entities.resend import ResendCodeEntity
from context.v1.codes.domain.usecase.resend import ResendCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router

if TYPE_CHECKING:
    from context.v1.emails.domain.entities.email import EmailEntity


@router.post(
    "/resend",
    summary="Resend code by email",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["Auth API"],
)
async def resend(
    request: Request,
    payload: ResendCodeDto,
):
    logger.info("Resend Code")

    entity: ResendCodeEntity = ResendCodeEntity(**payload.model_dump())

    use_case = ResendCodeUseCase(
        code_repository=CodeRepository(),
        email_repository=EmailRepository(),
        login_method_repository=LoginMethodRepository(),
    )

    new_entity: EmailEntity = use_case.execute(
        payload=entity
    )  # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    response = SignupEmailSchema(**new_entity.model_dump())

    return EnvelopeResponse(
        data=response.model_dump(),
        success=True,
        response_code=status.HTTP_200_OK,
    )
