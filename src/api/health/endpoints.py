from fastapi import APIRouter, status

from core.settings import settings
from core.utils.logger import logger
from core.utils.responses import EnvelopeResponse

router = APIRouter(tags=["Health Check"])

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health service",
    response_model=EnvelopeResponse,
)
def health_check() -> EnvelopeResponse:
    logger.info("Health")
    result = {
        "status": "ok",
        "message": "The service is online and functioning properly.",
        "timestamp": settings.TIMESTAP,
    }
    return EnvelopeResponse(
        errors=None,
        body=result,
        status_code=status.HTTP_200_OK,
        successful=True,
        message="The service is online and functioning properly.",
    )
