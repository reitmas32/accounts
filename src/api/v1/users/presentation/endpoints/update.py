from fastapi import Request, status

from api.v1.users.presentation.dtos import UpdateUserDto
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.put(
    "",
    summary="Actualizar registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def update(
    request: Request,
    payload: UpdateUserDto,
):
    log.info("Create User")
    return EnvelopeResponse(
        data=payload.model_dump(),
        response_code=status.HTTP_200_OK,
        success=True,
    )
