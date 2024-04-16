from fastapi import Header
from fastapi.requests import Request
from sqlalchemy import and_, select

from core.settings import settings
from core.settings.database import use_database_session
from core.utils.encryted import EncryptedController
from core.utils.exceptions import NotAuthorizationException
from models.service import ServiceModel


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
    if request.url.path.startswith("/api/v1/services"):
        return _check_root_authorization(
            X_API_Key=X_API_Key,
            X_Service_Name=X_Service_Name,
        )
    return _check_general_authorization(
        request=request,
        X_API_Key=X_API_Key,
        X_Service_Name=X_Service_Name,
    )


def _check_root_authorization(
    X_API_Key: str = "",  # noqa: N803
    X_Service_Name: str = "",  # noqa: N803,
):
    """
    Check root authorization for API requests.

    This function checks the root authorization headers provided in the request for API authentication.

    Args:
        X_API_Key (str): API key header.
        X_Service_Name (str): Service name header.

    Returns:
        bool: True if root authorization is successful, False otherwise.

    Raises:
        NotAuthorizationException: If root authorization fails.
    """
    if X_API_Key != settings.ROOT_API_KEY or X_Service_Name != settings.ROOT_SERVICE_NAME:
        raise NotAuthorizationException(resource="/api/v1/services")
    return True


def _check_general_authorization(
    request: Request,
    X_API_Key: str = "",  # noqa: N803
    X_Service_Name: str = "",  # noqa: N803,
):
    """
    Check general authorization for API requests.

    This function checks the general authorization headers provided in the request for API authentication.

    Args:
        request (Request): FastAPI request object.
        X_API_Key (str): API key header.
        X_Service_Name (str): Service name header.

    Returns:
        bool: True if general authorization is successful, False otherwise.

    Raises:
        NotAuthorizationException: If general authorization fails.
    """
    with use_database_session() as session:
        query = (
            select(ServiceModel)
            .where(
                and_(
                    ServiceModel.service_name == X_Service_Name,
                    ServiceModel.is_removed == False,  # noqa: E712
                )
            )
            .limit(1)
        )
        service: ServiceModel = session.execute(query).scalars().first()

        if service is None:
            raise NotAuthorizationException(resource=request.url.path)

        encrypted_controller = EncryptedController(key=settings.ROOT_ENCRYPTED_KEY)
        if X_API_Key != encrypted_controller.decrypt(encrypted_data=service.api_key.__str__()):
            raise NotAuthorizationException(resource=request.url.path)

    return True
