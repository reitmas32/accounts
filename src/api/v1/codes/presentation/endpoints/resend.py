from typing import TYPE_CHECKING

from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.v1.codes.presentation.dtos.resend import ResendCodeDto
from api.v1.emails.presentation.schemas.signup import SignupEmailSchema
from context.v1.codes.domain.entities.resend import ResendCodeEntity
from context.v1.codes.domain.usecase.resend import ResendCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_operations as router

if TYPE_CHECKING:
    from context.v1.emails.domain.entities.email import EmailEntity


@router.post(
    "/resend",
    summary="Resend code by email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def resend(
    payload: ResendCodeDto,
    session: Session = Depends(get_session)
):
    logger.info("Resend Code")

    entity: ResendCodeEntity = ResendCodeEntity(**payload.model_dump())

    use_case = ResendCodeUseCase(
        code_repository=CodeRepository(session=session),
        email_repository=EmailRepository(session=session),
        login_method_repository=LoginMethodRepository(session=session),
    )

    new_entity: EmailEntity = use_case.execute(
        payload=entity
    )  # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    response = SignupEmailSchema(**new_entity.model_dump())

    return ResponseEntity(data=response.model_dump(), code=StatusCodes.HTTP_200_OK)
