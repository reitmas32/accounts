from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from context.v1.roles.domain.usecase.retrive import RetriveRoleUseCase
from context.v1.roles.infrastructure.repositories.postgres.role import RoleRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router

if TYPE_CHECKING:
    from context.v1.roles.domain.entities.role import RoleEntity


@router.get(
    "/{id}",
    summary="Get a Role by ID",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_one(
    id: UUID,
    session: Session = Depends(get_session)

):
    logger.info("Get User")

    use_case = RetriveRoleUseCase(repository=RoleRepository(session=session))

    entity: RoleEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
