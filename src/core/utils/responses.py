# Standard Library
import decimal
import json
import uuid
from datetime import date, datetime
from typing import Any

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

class EnvelopeResponse(BaseModel):
    errors: Any | None = None
    body: EnvelopeResponseBody | ListEnvelopeResponseBody | dict | None = None


def create_envelope_response(data, links=None, count=None):
    body = EnvelopeResponseBody(links=links, count=count, results=data).model_dump()
    return EnvelopeResponse(errors=None, body=body)


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
