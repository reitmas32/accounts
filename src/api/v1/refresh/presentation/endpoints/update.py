from fastapi import Request, status

from api.v1.refresh.presentation.dtos import UpdateRefreshTokenDto
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router_crud as router


@router.put(
    "",
    summary="Update Refresh Token",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def update(
    request: Request,
    payload: UpdateRefreshTokenDto,
):
    log.info("Update Refresh Token")
    return EnvelopeResponse(
        data=payload.model_dump(),
        response_code=status.HTTP_200_OK,
        success=True,
    )
