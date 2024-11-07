from fastapi import Depends, Request, status

from api.v1.emails.presentation.dtos.filters import EmailFilters
from context.v1.emails.domain.usecase.list import ListEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)
from shared.app.use_cases.list import PaginationParams

from .routers import router


@router.get(
    "/",
    summary="Returns a list of emails",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    pagination_params: PaginationParams = Depends(),
    query_params: EmailFilters = Depends(),
):
    log.info("Get All Emails")

    filters = query_params.model_dump(exclude_unset=True, exclude_defaults=True)

    use_case = ListEmailUseCase(repository=EmailRepository())

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
