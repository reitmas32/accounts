from uuid import UUID

from fastapi import status

from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router_crud as router


@router.delete(
    "/{id}",
    summary="elimina un code",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def delte(
    id: UUID,
):
    logger.info("Delete Code")
