
from fastapi import Request, status

from api.v1.refresh.presentation.dtos import CreateRefreshTokenDto
from context.v1.refresh_token.domain.entities.refresh_token import RefreshTokenEntity
from context.v1.refresh_token.domain.usecase.create import CreateRefreshTokenUseCase
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_crud as router


@router.post(
    "",
    summary="Create a new refresh Token",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    request: Request,
    payload: CreateRefreshTokenDto,
):
    logger.info("Create Code")

    entity: RefreshTokenEntity = RefreshTokenEntity(**payload.model_dump())

    use_case = CreateRefreshTokenUseCase(repository=RefreshTokenRepository())

    new_entity: RefreshTokenEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
