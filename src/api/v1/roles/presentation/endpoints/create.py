
from fastapi import status

from api.v1.roles.presentation.dtos import CreateRoleDto
from context.v1.roles.domain.entities.role import RoleEntity
from context.v1.roles.domain.usecase.create import CreateRoleUseCase
from context.v1.roles.infrastructure.repositories.postgres.role import RoleRepository
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.post(
    "",
    summary="Create new Role",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    payload: CreateRoleDto,
):
    logger.info("Create Role")

    entity: RoleEntity = RoleEntity(**payload.model_dump())

    use_case = CreateRoleUseCase(repository=RoleRepository())

    new_entity: RoleEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
