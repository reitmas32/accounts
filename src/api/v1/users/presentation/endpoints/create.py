from fastapi import Request, status

from api.v1.users.crud.schemas import CreateUserSchema
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
    payload: CreateUserSchema,
):
    logger.info("Create User")
    return EnvelopeResponse(
        data=payload.model_dump(),
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
