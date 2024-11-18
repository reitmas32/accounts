from fastapi import Depends, Request, status

from api.v1.login_methods.presentation.dtos.filters import LoginMethodFilters
from context.v1.login_methods.domain.usecase.list import ListLoginMethodUseCase
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.get(
    "/",
    summary="Returns a list of login methods",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: LoginMethodFilters = Depends(),
):
    logger.info("Get All Login Methods")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListLoginMethodUseCase(repository=LoginMethodRepository())

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
