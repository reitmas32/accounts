import asyncio
import json
from collections.abc import Awaitable, Callable

import requests
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from core.settings import settings
from core.utils.logger import logger

background_tasks = set()

class WebHookDTO(BaseModel):
    resource: str
    response: dict


class CallWebHookMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[StreamingResponse]],
    ) -> Response:
        response = await call_next(request)
        path = request.url.path
        if path in settings.WEBHOOK_SIGNALS:
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            task = asyncio.create_task(
                CallWebHookMiddleware.call_webhook(
                    resource=path,
                    response=response_body[0].decode(),
                    # TODO: Add request: Taking into account that sensitive data must be deleted
                ),
            )

            background_tasks.add(task)

            task.add_done_callback(background_tasks.discard)
        return response

    @staticmethod
    async def call_webhook(resource: str, response: dict | None = None):
        # Simula una tarea que toma tiempo

        data_webhook = WebHookDTO(resource=resource, response=json.loads(response))
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        try:
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
        except requests.ConnectionError as e:
            logger.error(f"Error call the webhook {e}")

