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
    """
    Check authorization headers for API requests.

    This function checks the authorization headers provided in the request for API authentication.

    Args:
        request (Request): FastAPI request object.
        X_Service_Name (str): Service name header.
        X_API_Key (str): API key header.

    Returns:
        bool: True if authorization is successful, False otherwise.
    """
    url = settings.AUTH_MANAGER_URL
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = {
        "service_name": X_Service_Name,
        "api_key": X_API_Key,
    }

    response = requests.post(url, headers=headers, json=data, timeout=3000)
    if response.status_code != status.HTTP_201_CREATED:
        raise NotAuthorizationException(resource=request.url.path)
    return True
