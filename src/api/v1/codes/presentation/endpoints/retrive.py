from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import Depends, Request, status
from sqlalchemy.orm import Session

from context.v1.codes.domain.usecase.retrive import RetriveCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from core.settings import log
from core.settings.database import get_session
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router

if TYPE_CHECKING:
    from context.v1.codes.domain.entities.code import CodeEntity


@router.get(
    "/{id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_one(
    request: Request,
    id: UUID,
    session: Session = Depends(get_session),
):
    log.info("Get User")

    use_case = RetriveCodeUseCase(repository=CodeRepository())

    entity: CodeEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return EnvelopeResponse(
        data=data,
        response_code=status.HTTP_200_OK,
        success=True,
    )
