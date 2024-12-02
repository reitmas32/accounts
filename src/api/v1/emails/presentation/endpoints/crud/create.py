
from fastapi import Request, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.v1.emails.presentation.dtos import CreateEmailDto
from api.v1.emails.presentation.endpoints.routers import router_crud as router
from context.v1.emails.domain.entities.email import EmailEntity
from context.v1.emails.domain.usecase.create import CreateEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from core.settings.database import get_session
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
    session: Session = Depends(get_session)

):
    logger.info("Create Email")

    entity: EmailEntity = EmailEntity(**payload.model_dump())

    use_case = CreateEmailUseCase(repository=EmailRepository(session=session))

    new_entity: EmailEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
