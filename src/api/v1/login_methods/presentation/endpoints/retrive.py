from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status

from context.v1.login_methods.domain.usecase.retrive import RetriveLoginMethodUseCase
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_crud as router

if TYPE_CHECKING:
    from context.v1.codes.domain.entities.code import CodeEntity


@router.get(
    "/{id}",
    summary="Returns the login method",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_one(
    id: UUID,
):
    logger.info("Get Login Method")

    use_case = RetriveLoginMethodUseCase(repository=LoginMethodRepository())

    entity: CodeEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
