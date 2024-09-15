import json

from fastapi import APIRouter, status
from pydantic import BaseModel

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
    tags=["Health"],
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


class WebHookDTO(BaseModel):
    resource: str
    response: dict


@router.post(
    "/webhook-test",
    status_code=status.HTTP_200_OK,
    summary="Simple WebHook",
    tags=["WebHook"],
)
async def webhook(request: WebHookDTO):
    # Lee el cuerpo JSON recibido
    json_body = request.model_dump()

    logger.info(json.dumps(json_body, indent=2))

    # Retorna el mismo cuerpo JSON como respuesta
    return json_body
