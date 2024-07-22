from fastapi import APIRouter, Depends, Header, Request, status

from api.v1.platforms.logic.schemas import (
    SignInPlatformSchema,
    SignupPlatformSchema,
)
from api.v1.platforms.logic.services import (
    SignInPlatformService,
    SignUpPlatformService,
    VerifyJWTService,
)
from core.settings import log
from core.settings.database import use_database_session
from core.utils.autorization import check_authorization
from core.utils.responses import EnvelopeResponse

router = APIRouter(prefix="/platforms", tags=["Logic Platforms"])


@router.post(
    "/signup",
    summary="Create user registration via platform",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def platform_signup(
    request: Request,
    payload: SignupPlatformSchema,
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
        log.info("Signup with platform")
        return SignUpPlatformService(session=session).create(payload=payload)


@router.post(
    "/signin",
    summary="Signin user registration via platform",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
)
async def platform_signin(
    request: Request,
    payload: SignInPlatformSchema,
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
        log.info("Signup with platform")
        return SignInPlatformService(session=session).signin(payload=payload)


@router.get(
    "/verify-token",
    summary="Verify JWT via platform",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
)
async def verify_token(
    request: Request,
    auth: str = Header(),
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
    log.info("Verify JWT")
    return VerifyJWTService().verify_token(token=auth.split()[1])
