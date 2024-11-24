
from fastapi import Request, status

from api.v1.codes.presentation.dtos import CreateCodeDto
from context.v1.codes.domain.entities.code import CodeEntity
from context.v1.codes.domain.usecase.create import CreateCodeUseCase
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router


@router.post(
    "",
    summary="Crear registro de code",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def create(
    request: Request,
    payload: CreateCodeDto,
):
    logger.info("Create Code")

    entity: CodeEntity = CodeEntity(**payload.model_dump())

    use_case = CreateCodeUseCase(repository=CodeRepository())

    new_entity: CodeEntity = use_case.execute(payload=entity)

    return ResponseEntity(data=new_entity.model_dump(), code=StatusCodes.HTTP_201_CREATED)
