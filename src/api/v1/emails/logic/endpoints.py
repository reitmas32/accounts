from fastapi import APIRouter, Depends, Request, status

from api.v1.emails.logic.schemas import (
    LoginEmailSchema,
    SignupEmailSchema,
    VerifyEmailSchema,
)
from api.v1.emails.logic.services import (
    LoginEmailService,
    SignUpEmailService,
    VerifyCodeService,
)
from core.settings import log
from core.settings.database import use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import EnvelopeResponse

router = APIRouter(prefix="/emails", tags=["Logic emails"])


@router.post(
    "/signup",
    summary="Create user registration via email",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
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


@router.post(
    "/login",
    summary="Logea a un usuario por email y password",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
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
    "/verify",
    summary="Verifica un email enviando un correo con un codigo",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
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


@router.put(
    "/reset-password",
    summary="Logea a un usuario por email y password",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
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
    "/send-code",
    summary="Logea a un usuario por email y password",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def email_send_code(
    request: Request,
    payload: LoginEmailSchema,
    _=Depends(check_authorization),
):
    log.info("Login")
    with use_database_session() as session:
        return LoginEmailService(session=session).login(payload=payload)
