from fastapi import Header
from fastapi.requests import Request
from sqlalchemy import and_, select

from core.settings import settings
from core.settings.database import use_database_session
from core.utils.encryted import EncryptedController
from core.utils.exceptions import NotAuthorizationException
from models.service import ServiceModel


def check_autorization(
    request: Request,
    X_API_Key: str = Header(...),  # noqa: N803
    X_Service_Name: str = Header(...),  # noqa: N803
):
    if request.url.path.startswith("/api/v1/services"):
        return _check_root_autorization(
            X_API_Key=X_API_Key,
            X_Service_Name=X_Service_Name,
        )
    return _check_general_autorization(
        request=request,
        X_API_Key=X_API_Key,
        X_Service_Name=X_Service_Name,
    )


def _check_root_autorization(
    X_API_Key: str = "",  # noqa: N803
    X_Service_Name: str = "",  # noqa: N803,
):
    if (
        X_API_Key != settings.ROOT_API_KEY
        or X_Service_Name != settings.ROOT_SERVICE_NAME
    ):
        raise NotAuthorizationException(resource="/api/v1/services")
    return True


def _check_general_autorization(
    request: Request,
    X_API_Key: str = "",  # noqa: N803
    X_Service_Name: str = "",  # noqa: N803,
):
    with use_database_session() as session:
        query = (
            select(ServiceModel)
            .where(
                and_(
                    ServiceModel.service_name == X_Service_Name,
                    ServiceModel.is_removed is False,
                )
            )
            .limit(1)
        )
        service: ServiceModel = session.execute(query).scalars().first()

        if service is None:
            raise NotAuthorizationException(resource=request.url.path)

        encrypted_controller = EncryptedController(key=settings.ROOT_ENCRYPTED_KEY)
        if X_API_Key != encrypted_controller.decrypt(
            encrypted_data=service.api_key.__str__()
        ):
            raise NotAuthorizationException(resource=request.url.path)

    return True
