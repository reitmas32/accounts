from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.emails.presentation.dtos.filters import EmailFilters
from api.v1.emails.presentation.endpoints.routers import router_crud as router
from context.v1.emails.domain.usecase.list import ListEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.app.use_cases.list import PaginationParams
from shared.presentation.schemas.envelope_response import ResponseEntity


@router.get(
    "",
    summary="Returns a list of emails",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: EmailFilters = Depends(),
    session: Session = Depends(get_session)

):
    logger.info("Get All Emails")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListEmailUseCase(repository=EmailRepository(session=session))

    entities = use_case.execute(
        filters=filters,
        pagination_params=pagination_params,
        url=request.url,
    )

    return ResponseEntity(data=entities, code=StatusCodes.HTTP_200_OK)
