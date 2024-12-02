from typing import TYPE_CHECKING
from uuid import UUID

from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from context.v1.users.domain.usecase.retrive import RetriveUserUseCase
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router

if TYPE_CHECKING:
    from context.v1.users.domain.entities.user import UserEntity


@router.get(
    "/{id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def retrieve_one(
    id: UUID,
    session: Session = Depends(get_session)
):
    logger.info("Get User")

    use_case = RetriveUserUseCase(repository=UserRepository(session=session))

    entity: UserEntity | None = use_case.execute(id=id)

    data = None

    if entity is not None:
        data = entity.model_dump()

    return ResponseEntity(data=data, code=StatusCodes.HTTP_200_OK)
