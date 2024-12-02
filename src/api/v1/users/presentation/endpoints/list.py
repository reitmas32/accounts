from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.users.presentation.dtos.filters import UserFilters
from context.v1.users.domain.usecase.list import ListUserUseCase
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.settings import log
from core.settings.database import get_session
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.get(
    "",
    summary="Returns a list of users",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: UserFilters = Depends(),
    session: Session = Depends(get_session)
):
    log.info("Get All Users")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListUserUseCase(repository=UserRepository(session=session))

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
