from fastapi import Depends, Request, status

from api.v1.platforms.presentation.dtos.filters import PlatformFilters
from api.v1.platforms.presentation.endpoints.routers import router_crud as router
from context.v1.platforms.domain.usecase.list import ListPlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity


@router.get(
    "",
    summary="Returns a list of platforms",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: PlatformFilters = Depends(),
):
    logger.info("Get All platforms")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListPlatformUseCase(repository=PlatformRepository())

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
