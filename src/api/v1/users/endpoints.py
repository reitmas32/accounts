from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from api.v1.users.schemas import SignupEmailSchema, VerifyEmailSchema
from api.v1.users.services import (
    RetrieveUserService,
    SignUpEmailService,
)
from api.v1.users.services.login_email import LoginEmailSchema, LoginEmailService
from api.v1.users.services.verify import VerifyCodeService
from core.settings import log
from core.settings.database import get_session, use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import (
    EnvelopeResponse,
)

router = APIRouter(prefix="/users")


@router.get(
    "/",
    summary="Returns a list of users",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["users"],
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
    tags=["users"],
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
    "/email/signup",
    summary="Create user registration via email",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_signup(
    request: Request,
    payload: SignupEmailSchema,
    _=Depends(check_authorization),
):
    """
    Create a user registration via email.

    This endpoint allows the creation of a user account using email as the authentication method.

    Args:
        request (Request): FastAPI request object.
        payload (SignupEmailSchema): Data payload containing email signup information.
        _: Dependency to check authorization (ignored).

    Returns:
        dict: Envelope response containing user data, message, and status code.
    """
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return SignUpEmailService(session=session).create(payload=payload)


@router.put(
    "/email/verify",
    summary="Verifica un email enviando un correo con un codigo",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_verify(
    request: Request,
    payload: VerifyEmailSchema,
    _=Depends(check_authorization),
):
    """
    Create a user registration via email.\n

    This endpoint allows the creation of a user account using email as the authentication method.

    Args:
        request (Request): FastAPI request object.\n
        payload (SignupEmailSchema): Data payload containing email signup information.\n
        _: Dependency to check authorization (ignored).\n

    Returns:
        dict: Envelope response containing user data, message, and status code\n.
    """
    log.info("Create User")
    with use_database_session() as session:
        log.info("Create a DisbursementPeriod")
        return VerifyCodeService(session=session).verify(payload=payload)


@router.post(
    "/email/login",
    summary="Logea a un usuario por email y password",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_login(
    request: Request,
    payload: LoginEmailSchema,
    _=Depends(check_authorization),
):
    log.info("Login")
    with use_database_session() as session:
        return LoginEmailService(session=session).login(payload=payload)


@router.put(
    "/email/reset-password",
    summary="Logea a un usuario por email y password",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_reset_password(
    request: Request,
    payload: LoginEmailSchema,
    _=Depends(check_authorization),
):
    log.info("Login")
    with use_database_session() as session:
        return LoginEmailService(session=session).login(payload=payload)


@router.post(
    "/email/send-code",
    summary="Logea a un usuario por email y password",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["email"],
)
async def email_send_code(
    request: Request,
    payload: LoginEmailSchema,
    _=Depends(check_authorization),
):
    log.info("Login")
    with use_database_session() as session:
        return LoginEmailService(session=session).login(payload=payload)
