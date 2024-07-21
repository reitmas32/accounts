from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from core.clients.auth.client import AuthServiceClient
from core.clients.auth.schemas import AuthSchema
from core.settings import settings
from core.utils.exceptions import NotAuthorizationException
from core.utils.logger import logger
from shared.exceptions import NotAuthorizedError

auth_client = AuthServiceClient()


class AuthenticationMiddelware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not settings.AUTHTENTICATION_ACTIVE:
            return await call_next(request)

        path = request.url.path.rstrip("/") # /accounts/docs -> /docs
        logger.info(f"The Path is {path}")
        try:
            if path not in settings.PUBLIC_ENDPOINTS:
                service_name = request.headers.get("x-service-name", "")
                api_key = request.headers.get("x-api-key", "")
                auth_client.validate(
                    resource=path,
                    payload=AuthSchema(
                        service_name=service_name,
                        api_key=api_key,
                    ),
                )
            else:
                logger.info(f"The endpoint {path} is public")
        except NotAuthorizedError as e:
            raise NotAuthorizationException(resource=request.url.path, message=str(e))

        return await call_next(request)
