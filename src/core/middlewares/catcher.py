from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from starlette.middleware.base import BaseHTTPMiddleware

from core.utils.exceptions import BaseAppException
from core.utils.responses import EnvelopeResponse


class CatcherExceptionsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:  # noqa: BLE001
            if isinstance(e, HTTPException):
                error_detail = {"detail": str(e.detail)}
                status_code = e.status_code
            if isinstance(e, NoResultFound):
                error_detail = {"detail": f"No found: {e}"}
                status_code = status.HTTP_404_NOT_FOUND
            elif isinstance(e, BaseAppException):
                error_detail = e.to_dict()
                status_code = e.status_code
            else:
                error_detail = {"detail": str(e)}
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            response = EnvelopeResponse(
                errors=error_detail,
                body=None,
                message=str(e),
                status_code=status_code,
                successful=False,
            )
            return JSONResponse(status_code=status_code, content=dict(response))
