
from fastapi import Request, status

from api.v1.login_methods.presentation.dtos import CreateLoginMethodDto
from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from context.v1.login_methods.domain.usecase.create import CreateLoginMethodUseCase
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_crud as router


@router.post(
    "",
    summary="Crear registro de login method",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    request: Request,
    payload: CreateLoginMethodDto,
):
    logger.info("Create Login Method")

    entity: LoginMethodEntity = LoginMethodEntity(**payload.model_dump())

    use_case = CreateLoginMethodUseCase(repository=LoginMethodRepository())

    new_entity: LoginMethodEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
