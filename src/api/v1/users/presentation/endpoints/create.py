
from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.v1.users.presentation.dtos import CreateUserDto
from context.v1.users.domain.entities.user import UserEntity
from context.v1.users.domain.usecase.create import CreateUserUseCase
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    payload: CreateUserDto,
    session: Session = Depends(get_session)

):
    logger.info("Create User")

    entity: UserEntity = UserEntity(**payload.model_dump())

    use_case = CreateUserUseCase(repository=UserRepository(session=session))

    new_entity: UserEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
