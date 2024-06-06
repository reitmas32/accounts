import logging

import requests
from pydantic import BaseModel

from shared.constants import MethodType, ReturnType
from shared.exceptions import APIExceptionError, RequestExceptionError

logger = logging.getLogger(__name__)


class APIRestClient:
    def __init__(self):
        self.session = self._init_session()

    def _get_headers(self):
        return {
            "Cache-Control": "no-cache",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        }

    def _init_session(self) -> requests.Session:
        headers = self._get_headers()
        session = requests.session()
        session.headers.update(headers)
        return session

    def _request(
        self,
        url: str,
        data: dict = {},  # noqa: B006
        method: MethodType = MethodType.GET,
        return_type: ReturnType = ReturnType.PROCESSED,
        *args,
        **kwargs,
    ):
        response = getattr(self.session, method)(
            url,
            data=data,
            verify=True,
            timeout=3000,
            headers={
                # "x-trace-id": "fsdas",
                # "x-caller-id": settings.PROJECT_ID
            },
            *args,  # noqa: B026
            **kwargs,
        )
        if return_type == ReturnType.FULL:
            return response
        return self._handle_response(response)

    @staticmethod
    def _handle_response(response: requests.Response):
        """Internal helper for handling API responses from the sw.com.mx server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """
        if not (requests.codes["ok"] <= response.status_code < requests.codes["multiple_choices"]):
            raise APIExceptionError(response)
        try:
            response_json = response.json()
            body = response_json.get("body")
            if not body:
                return body
            return body.get("results")
        except ValueError:
            raise RequestExceptionError(f"Invalid Response: {response.text}")

    def handle_params(self, filters: BaseModel | None = None):
        params = {}
        if isinstance(filters, BaseModel):
            params = filters.model_dump()
        return params
