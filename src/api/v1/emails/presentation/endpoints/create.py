
from fastapi import Request, status

from api.v1.emails.presentation.dtos import CreateEmailDto
from context.v1.emails.domain.entities.email import EmailEntity
from context.v1.emails.domain.usecase.create import CreateEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.post(
    "",
    summary="Crear registro de email",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateEmailDto,
):
    logger.info("Create Email")

    entity: EmailEntity = EmailEntity(**payload.model_dump())

    use_case = CreateEmailUseCase(repository=EmailRepository())

    new_entity: EmailEntity = use_case.execute(payload=entity) # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    return EnvelopeResponse(
        data=new_entity.model_dump(),
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
