from fastapi import Depends, Request, status

from api.v1.codes.presentation.dtos.filters import CodeFilters
from context.v1.codes.domain.usecase.list import ListCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)
from shared.app.use_cases.list import PaginationParams

from .routers import router


@router.get(
    "/",
    summary="Returns a list of codes",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: CodeFilters = Depends(),
):
    log.info("Get All Codes")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListCodeUseCase(repository=CodeRepository())

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
