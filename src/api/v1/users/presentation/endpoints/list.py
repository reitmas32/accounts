from fastapi import Depends, Request, status

from api.v1.users.presentation.dtos.filters import UserFilters
from context.v1.users.domain.usecase.list import ListUserUseCase
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)
from shared.app.use_cases.list import PaginationParams

from .routers import router


@router.get(
    "/",
    summary="Returns a list of users",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: UserFilters = Depends(),
):
    log.info("Get All Users")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListUserUseCase(repository=UserRepository())

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
