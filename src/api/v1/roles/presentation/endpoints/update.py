from fastapi import Request, status

from api.v1.roles.presentation.dtos import UpdateRoleDto
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.put(
    "",
    summary="Update fields of Role",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def update(
    request: Request,
    payload: UpdateRoleDto,
):
    log.info("Update fields of Role")
    return EnvelopeResponse(
        data=payload.model_dump(),
        response_code=status.HTTP_200_OK,
        success=True,
    )
