
from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import Request, status

from api.v1.platforms.presentation.endpoints.routers import router
from context.v1.platforms.domain.usecase.retrive import RetrivePlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)

if TYPE_CHECKING:
    from context.v1.platforms.domain.entities.platform import PlatformEntity


@router.get(
    "/{id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_one(
    request: Request,
    id: UUID,
):
    log.info("Get User")

    use_case = RetrivePlatformUseCase(repository=PlatformRepository())

    entity: PlatformEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return EnvelopeResponse(
        data=data,
        response_code=status.HTTP_200_OK,
        success=True,
    )
