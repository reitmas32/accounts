# Standard Library
import decimal
import json
import uuid
from datetime import date, datetime
from typing import Any

from fastapi import Query, status
from fastapi_pagination.default import OptionalParams

# Third Party Stuff
from pydantic import BaseModel, HttpUrl
from pytz import timezone

from core.settings import settings


class Links(BaseModel):
    next: HttpUrl | None = None
    previous: HttpUrl | None = None


class EnvelopeResponseBody(BaseModel):
    links: Any | None = None
    count: Any | None = None
    results: Any | None = None


class ListEnvelopeResponseBody(EnvelopeResponseBody):
    results: list | None = None


class SimpleEnvelopeResponseBody(BaseModel):
    results: list | None = None


class EnvelopeResponse(BaseModel):
    errors: Any | None = None
    message: str | None = None
    response_code: int
    internal_code: int | None = None
    external_code: int | None = None
    success: bool

    data: str | dict | EnvelopeResponseBody | ListEnvelopeResponseBody | None = None


def create_envelope_response(  # noqa: PLR0913
    data,
    links=None,
    count=None,
    message: str = "INTERNAL_SERVER_ERROR",
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    successful: bool = False,  # noqa: FBT001
):
    body = EnvelopeResponseBody(links=links, count=count, results=data).model_dump()
    return EnvelopeResponse(
        errors=None,
        data=body,
        message=message,
        response_code=status_code,
        success=successful,
    )


def create_simple_envelope_response(
    data,
    message: str = "INTERNAL_SERVER_ERROR",
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    successful: bool = False,  # noqa: FBT001
):
    return EnvelopeResponse(
        errors=None,
        data=data,
        message=message,
        response_code=status_code,
        success=successful,
    )


def get_current_date_time_to_app_standard() -> datetime:
    return datetime.now(timezone(settings.TIME_ZONE))


def get_current_date_time_utc() -> datetime:
    return datetime.now(timezone(settings.TIME_ZONE_UTC))


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, date):
            return obj.isoformat()

        if isinstance(obj, decimal.Decimal):
            return float(obj)

        return json.JSONEncoder.default(self, obj)


class PaginationParams(OptionalParams):
    size: int | None = Query(None, ge=0, le=500, description="Page size")


def default_pagination_params(
    page: int = Query(1, ge=1, alias="page", description="Page number"),
    page_size: int = Query(
        settings.DEFAULT_PAGE_SIZE,
        ge=0,
        le=500,
        alias="page_size",
        description="Page size",
    ),
) -> PaginationParams:
    return PaginationParams(page=page, size=page_size)


class FilterBaseSchema(BaseModel):
    ordering: str | None = settings.DEFAULT_ORDER_FIELD
