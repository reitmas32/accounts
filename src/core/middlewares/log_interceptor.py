import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from core.utils.logger import logger


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("x-trace-id", str(uuid.uuid4()))
        caller_id = request.headers.get("x-caller-id", "000000")

        logger.info(f"Received request {request.method} {request.url}")

        with logger.contextualize(trace_id=trace_id, caller_id=caller_id):
            response = await call_next(request)
            logger.info("Request ended")
            return response
