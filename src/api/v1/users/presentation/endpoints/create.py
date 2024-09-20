
from fastapi import Request, status

from api.v1.users.domain.entities.user import UserEntity
from api.v1.users.domain.usecase.create import CreateUserUseCase
from api.v1.users.infrastructure.repositories.postgres.user import UserRepository
from api.v1.users.presentation.dtos import CreateUserDto
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateUserDto,
):
    logger.info("Create User")

    entity: UserEntity = UserEntity(**payload.model_dump())

    use_case = CreateUserUseCase(repository=UserRepository())

    new_entity: UserEntity = use_case.execute(payload=entity) # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    return EnvelopeResponse(
        data=new_entity.model_dump(),
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
