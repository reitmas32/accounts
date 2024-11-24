
from fastapi import Request, status

from api.v1.emails.presentation.dtos import CreateEmailDto
from api.v1.emails.presentation.endpoints.routers import router_crud as router
from context.v1.emails.domain.entities.email import EmailEntity
from context.v1.emails.domain.usecase.create import CreateEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity


@router.post(
    "",
    summary="Crear registro de email",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    request: Request,
    payload: CreateEmailDto,
):
    logger.info("Create Email")

    entity: EmailEntity = EmailEntity(**payload.model_dump())

    use_case = CreateEmailUseCase(repository=EmailRepository())

    new_entity: EmailEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
