from fastapi import Request, status

from api.v1.codes.presentation.dtos import UpdateCodeDto
from api.v1.emails.presentation.endpoints.routers import router
from core.settings import log
from core.utils.responses import (
    EnvelopeResponse,
)


@router.put(
    "",
    summary="Actualizar registro de code",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def update(
    request: Request,
    payload: UpdateCodeDto,
):
    log.info("Create Code")
    return EnvelopeResponse(
        data=payload.model_dump(),
        response_code=status.HTTP_200_OK,
        success=True,
    )
