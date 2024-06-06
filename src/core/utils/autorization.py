import requests
from fastapi import Header, status
from fastapi.requests import Request

from core.settings import settings
from core.utils.exceptions import NotAuthorizationException


def check_authorization(
    request: Request,
    X_Service_Name: str = Header(...),  # noqa: N803
    X_API_Key: str = Header(...),  # noqa: N803
):
    pass
