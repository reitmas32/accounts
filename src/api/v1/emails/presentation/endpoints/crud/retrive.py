from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status

from api.v1.emails.presentation.endpoints.routers import router
from context.v1.emails.domain.usecase.retrive import RetriveEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

if TYPE_CHECKING:
    from context.v1.codes.domain.entities.code import CodeEntity


@router.get(
    "/{id}",
    summary="Returns the email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_one(
    id: UUID,
):
    logger.info("Get Email")

    use_case = RetriveEmailUseCase(repository=EmailRepository())

    entity: CodeEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
