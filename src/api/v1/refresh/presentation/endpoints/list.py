from fastapi import Depends, Request, status

from api.v1.refresh.presentation.dtos.filters import RefreshTokenFilters
from context.v1.refresh_token.domain.usecase.list import ListRefreshTokenUseCase
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_crud as router


@router.get(
    "",
    summary="Returns a list of codes",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: RefreshTokenFilters = Depends(),
):
    logger.info("Get All Codes")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListRefreshTokenUseCase(repository=RefreshTokenRepository())

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
