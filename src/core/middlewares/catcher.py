from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from starlette.middleware.base import BaseHTTPMiddleware

from core.utils.responses import EnvelopeResponse
from shared.app.errors.base import BaseError


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
            elif isinstance(e, IntegrityError):
                error_detail = e.orig
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                if isinstance(e.orig, ForeignKeyViolation):
                    err = e.orig
                    error_detail = {f"{err.diag.table_name}": f"ForeignKeyViolation: {err.diag.table_name}"}
                    status_code = status.HTTP_409_CONFLICT
                    e = f"ForeignKeyViolation: {err.diag.table_name}"
            elif isinstance(e, BaseError):
                error_detail = e.to_dict()
                status_code = e.external_code.http
            else:
                error_detail = {"detail": str(e)}
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            internal_code = e.internal_code if hasattr(e, "internal_code") else status_code
            external_code = e.external_code if hasattr(e, "external_code") else status_code

            response = EnvelopeResponse(
                errors=error_detail,
                data=None,
                message=str(e),
                response_code=status_code,
                success=False,
                internal_code=internal_code,
                external_code=external_code,
            )
            return JSONResponse(status_code=status_code, content=dict(response))
