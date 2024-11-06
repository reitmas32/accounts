from fastapi import Depends, Request, status

from api.v1.platforms.presentation.dtos.filters import PlatformFilters
from api.v1.platforms.presentation.endpoints.routers import router
from context.v1.platforms.domain.usecase.list import ListPlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)
from shared.app.use_cases.list import PaginationParams


@router.get(
    "/",
    summary="Returns a list o1.platforms",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: PlatformFilters = Depends(),
):
    log.info("Get Al1.platforms")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListPlatformUseCase(repository=PlatformRepository())

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return EnvelopeResponse(
        errors=None,
        data=entities.model_dump(),
        response_code=status.HTTP_200_OK,
        success=True,
    )
