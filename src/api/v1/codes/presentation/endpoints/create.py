
from fastapi import Request, status

from api.v1.codes.domain.entities.code import CodeEntity
from api.v1.codes.domain.usecase.create import CreateCodeUseCase
from api.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from api.v1.codes.presentation.dtos import CreateCodeDto
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.post(
    "",
    summary="Crear registro de code",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateCodeDto,
):
    logger.info("Create Code")

    entity: CodeEntity = CodeEntity(**payload.model_dump())

    use_case = CreateCodeUseCase(repository=CodeRepository())

    new_entity: CodeEntity = use_case.execute(payload=entity) # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    return EnvelopeResponse(
        data=new_entity.model_dump(),
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
