
from fastapi import Request, status

from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from context.v1.login_methods.domain.usecase.create import CreateLoginMethodUseCase
from api.v1.login_methods.presentation.dtos import CreateLoginMethodDto
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.post(
    "",
    summary="Crear registro de login method",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateLoginMethodDto,
):
    logger.info("Create Login Method")

    entity: LoginMethodEntity = LoginMethodEntity(**payload.model_dump())

    use_case = CreateLoginMethodUseCase(repository=LoginMethodRepository())

    new_entity: LoginMethodEntity = use_case.execute(payload=entity) # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    return EnvelopeResponse(
        data=new_entity.model_dump(),
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
