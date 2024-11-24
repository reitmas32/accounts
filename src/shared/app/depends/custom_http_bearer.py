
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from shared.app.errors.authorization_token import AthorizationHeaderError


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        if "authorization" not in request.headers:
            raise AthorizationHeaderError
        return await super().__call__(request)
