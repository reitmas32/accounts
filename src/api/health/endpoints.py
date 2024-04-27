from datetime import datetime

from fastapi import APIRouter, status

from core.settings import settings
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
    result = {
        "status": "ok",
        "message": "The service is online and functioning properly.",
        "timestamp": datetime.now().astimezone().strftime(format=settings.DATE_TIME_FORMAT),
    }
    return EnvelopeResponse(
        errors=None,
        body=result,
        status_code=status.HTTP_200_OK,
        successful=True,
        message="The service is online and functioning properly.",
    )
