# myapp/middlewares.py


from http import HTTPStatus
from typing import TYPE_CHECKING

from core.clients.auth.schemas import AuthSchema
from core.settings import settings
from core.utils.logger import logger
from shared.app.errors import APIError, NotAuthorizedError
from shared.client import APIRestClient
from shared.constants import MethodType, ReturnType

if TYPE_CHECKING:
    import requests


class AuthServiceClient(APIRestClient):
    BASE_URL: str = (
        settings.AUTH_SERVICE_API_HOST
        + "/api"
        + f"/{settings.AUTH_SERVICE_API_VERSION}"
        + f"/{settings.AUTH_SERVICE_API_PREFIX}"
    )

    def validate(self, resource: str, payload: AuthSchema):
        url = f"{self.BASE_URL}/validate"
        try:
            logger.info(f"Request to URL: {url}")
            response: requests.Response = self._request(
                url,
                method=MethodType.POST,
                data=payload.model_dump_json(exclude_none=True),
                return_type=ReturnType.FULL,
            )
            logger.info(f"Response: {response}")
            if response is None:
                logger.error(f"Error to Auth service in {url}")
            if response.status_code != HTTPStatus.CREATED:
                logger.error("Dont Autorization Service to resource")
                raise NotAuthorizedError(resource)

        except APIError as e:
            logger.info(f"Response: {e.response}")
            response = None
        return response
