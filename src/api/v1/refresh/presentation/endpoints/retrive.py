from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status

from context.v1.refresh_token.domain.usecase.retrive import RetriveRefreshTokenUseCase
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_crud as router

if TYPE_CHECKING:
    from context.v1.refresh_token.domain.entities.refresh_token import (
        RefreshTokenEntity,
    )


@router.get(
    "/{id}",
    summary="Get RefreshToken by ID",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_one(
    id: UUID,
):
    logger.info("Get RefreshToken")

    use_case = RetriveRefreshTokenUseCase(repository=RefreshTokenRepository())

    entity: RefreshTokenEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
