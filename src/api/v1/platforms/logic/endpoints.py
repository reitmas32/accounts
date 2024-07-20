from fastapi import APIRouter, Depends, Request, status

from api.v1.emails.logic.schemas import (
    SignupEmailSchema,
)
from api.v1.emails.logic.services import (
    SignUpEmailService,
)
from api.v1.platforms.logic.schemas import SignupPlatformSchema
from api.v1.platforms.logic.services import SignUpPlatformService
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

