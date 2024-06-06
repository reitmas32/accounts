import logging

import requests

logger = logging.getLogger(__name__)


class APIExceptionError(Exception):
    def __init__(self, response: requests.Response):
        try:
            self.message = response.json().get("errors")
        except ValueError:
            self.message = f"Invalid JSON error message: {response.text}"
        except Exception as exc:  # noqa: BLE001
            logger.info(exc)
            self.message = exc

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, "request", None)

    def __str__(self):
        return f"APIError(code={self.status_code}): {self.message}"


class RequestExceptionError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"RequestExceptionError: {self.message}"


class NotAuthorizedError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"NotAuthorizedError: {self.message}"


class GRPCException(Exception):  # noqa: N818
    pass


class UnimplementedError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"UnimplementedError: {self.message}"
