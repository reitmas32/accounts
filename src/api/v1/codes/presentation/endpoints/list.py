from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.codes.presentation.dtos.filters import CodeFilters
from context.v1.codes.domain.usecase.list import ListCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.get(
    "",
    summary="Returns a list of codes",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: CodeFilters = Depends(),
    session: Session = Depends(get_session)

):
    logger.info("Get All Codes")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListCodeUseCase(repository=CodeRepository(session=session))

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
