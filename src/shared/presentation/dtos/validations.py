from collections import defaultdict

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from core.utils.responses import EnvelopeResponse


def validation_pydantic_field(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validate(_: Request, exc: Exception):
        error_detail = defaultdict(list)
        for error in exc.errors():
            field = error["loc"][1] if "loc" in error else None
            error_msg = error["msg"]
            error_detail[field].append(error_msg)

        response = EnvelopeResponse(
            errors=error_detail, data=None, response_code=status.HTTP_400_BAD_REQUEST, success=False, message=error_msg
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=dict(response),
        )
