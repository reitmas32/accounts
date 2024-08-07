from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.codes.crud.services import DeleteCodesService
from api.v1.users.crud.schemas import CreateUserSchema
from api.v1.users.crud.services import CreateUserService, RetrieveUserService
from core.settings import log
from core.settings.database import get_session, use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import (
    EnvelopeResponse,
)

router = APIRouter(prefix="/users", tags=["CRUD users"])


@router.get(
    "/",
    summary="Returns a list of users",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_all(
    request: Request,
    _=Depends(check_authorization),
    session: Session = Depends(get_session),
):
    """
    Retrieve all users.

    This endpoint retrieves information for all users in the database.

    Args:
        request (Request): FastAPI request object.
        _: Dependency to check authorization (ignored).
        session (Session): Database session for interacting with the data.

    Returns:
        dict: Envelope response containing user data, count, message, and status code.
    """
    log.info("Get User")
    return RetrieveUserService(session=session).retrieve_all()


@router.get(
    "/{user_id}",
    summary="Returns the data of the authenticated user",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def retrieve_one(
    request: Request,
    user_id: UUID,
    _=Depends(check_authorization),
    session: Session = Depends(get_session),
):
    """
    Retrieve data of the authenticated user.

    This endpoint retrieves information of the authenticated user by user ID.

    Args:
        request (Request): FastAPI request object.
        user_id (UUID): ID of the user to retrieve.
        _: Dependency to check authorization (ignored).
        session (Session): Database session for interacting with the data.

    Returns:
        dict: Envelope response containing user data, count, message, and status code.
    """
    log.info("Get User")
    return RetrieveUserService(session=session).retrieve_by_id(id=user_id)


@router.post(
    "",
    summary="Crear registro de usuario",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def create(
    request: Request,
    payload: CreateUserSchema,
    _=Depends(check_authorization),
):
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a User")
        return CreateUserService(session=session).create(payload=payload)


@router.delete(
    "/{id}",
    summary="elimina un usuario",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def delte(
    id: UUID,
    _=Depends(check_authorization),
):
    with use_database_session() as session:
        log.info("Get only one Service")
        return DeleteCodesService(session=session).delete(id=id)




@router.get(
    "/ceo",
)
async def retrieve_one(
    request: Request,
):
    log.info("Get User")
    return {
        "name":"Alex"
    }
