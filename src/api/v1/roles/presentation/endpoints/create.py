
from fastapi import Depends, status
from sqlalchemy.orm import Session

from api.v1.roles.presentation.dtos import CreateRoleDto
from context.v1.roles.domain.entities.role import RoleEntity
from context.v1.roles.domain.usecase.create import CreateRoleUseCase
from context.v1.roles.infrastructure.repositories.postgres.role import RoleRepository
from core.settings.database import get_session
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
    session: Session = Depends(get_session)
):
    logger.info("Create Role")

    entity: RoleEntity = RoleEntity(**payload.model_dump())

    use_case = CreateRoleUseCase(repository=RoleRepository(session=session))

    new_entity: RoleEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
