from fastapi import status

from api.v1.platforms.presentation.dtos import CreatePlatformDto
from api.v1.platforms.presentation.endpoints.routers import router_crud as router
from context.v1.platforms.domain.entities.platform import PlatformEntity
from context.v1.platforms.domain.usecase.create import CreatePlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity


@router.post(
    "",
    summary="Crear registro de platform",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    payload: CreatePlatformDto,
):
    logger.info("Create Platform")

    entity: PlatformEntity = PlatformEntity(**payload.model_dump())

    use_case = CreatePlatformUseCase(repository=PlatformRepository())

    new_entity: PlatformEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
