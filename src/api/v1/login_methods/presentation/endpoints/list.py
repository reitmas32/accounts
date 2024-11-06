from fastapi import Depends, Request, status

from context.v1.login_methods.domain.usecase.list import ListLoginMethodUseCase
from api.v1.login_methods.presentation.dtos.filters import LoginMethodFilters
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)
from shared.app.use_cases.list import PaginationParams

from .routers import router


@router.get(
    "/",
    summary="Returns a list of login methods",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: LoginMethodFilters = Depends(),
):
    log.info("Get All Login Methods")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListLoginMethodUseCase(repository=LoginMethodRepository())

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
