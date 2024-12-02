
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.v1.platforms.presentation.endpoints.routers import router_crud as router
from context.v1.platforms.domain.usecase.retrive import RetrivePlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

if TYPE_CHECKING:
    from context.v1.platforms.domain.entities.platform import PlatformEntity


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

    use_case = RetrivePlatformUseCase(repository=PlatformRepository(session=session))

    entity: PlatformEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
