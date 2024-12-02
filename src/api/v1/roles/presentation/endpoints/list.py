from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.roles.presentation.dtos.filters import RoleFilters
from context.v1.roles.domain.usecase.list import ListRoleUseCase
from context.v1.roles.infrastructure.repositories.postgres.role import RoleRepository
from core.settings import log
from core.settings.database import get_session
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.get(
    "",
    summary="Returns a list of roles",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: RoleFilters = Depends(),
    session: Session = Depends(get_session)

):
    log.info("Get All Roles")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListRoleUseCase(repository=RoleRepository(session=session))

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
