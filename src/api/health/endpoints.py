from fastapi import APIRouter, status
from core.settings import settings
from core.utils.responses import EnvelopeResponse, EnvelopeResponseBody

router = APIRouter(tags=["Health Check"])


@router.get(
    "/health", status_code=status.HTTP_200_OK, summary="Health service", response_model=EnvelopeResponse
)
def health_check() -> EnvelopeResponse:
    result = {
        'status' : 'ok'
    }
    body = EnvelopeResponseBody(links=None, count=None, results=result)
    return EnvelopeResponse(errors=None, body=body)
