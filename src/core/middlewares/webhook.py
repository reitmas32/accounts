import json

import requests
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from core.settings import settings
from core.utils.logger import logger


class WebHookDTO(BaseModel):
    resource: str
    response: dict


class CallWebHookMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        path = request.url.path
        if path in settings.WEBHOOK_SIGNALS and isinstance(response, StreamingResponse):
            # Consumir el contenido de la respuesta
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Intentar decodificar el cuerpo de la respuesta como JSON
            try:
                json_response = json.loads(response_body.decode())
                data_webhook = WebHookDTO(resource=path, response=json_response)
                headers = {
                    "accept": "application/json",
                    "Content-Type": "application/json",
                }

                requests.post(  # noqa: ASYNC210
                    settings.WEBHOOK,
                    headers=headers,
                    json=data_webhook.model_dump(),
                    timeout=0.001,
                )

            except json.JSONDecodeError:
                logger.error("Error call the webhook")
            except requests.Timeout:
                pass

            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        return response
