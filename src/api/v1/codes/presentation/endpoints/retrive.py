from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from context.v1.codes.domain.usecase.retrive import RetriveCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router

if TYPE_CHECKING:
    from context.v1.codes.domain.entities.code import CodeEntity


@router.get(
    "/{id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_one(
    id: UUID,
    session: Session = Depends(get_session)

):
    logger.info("Get User")

    use_case = RetriveCodeUseCase(repository=CodeRepository(session=session))

    entity: CodeEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
