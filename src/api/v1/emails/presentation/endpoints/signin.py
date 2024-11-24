from fastapi import Request, status

from api.v1.emails.presentation.dtos.signin import SigninEmailDto
from context.v1.emails.domain.entities.signin import SigninEmailEntity
from context.v1.emails.domain.usecase.signin import SignInWithEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_operations as router


@router.post(
    "/signin",
    summary="SignIn user with email",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def signup(
    request: Request,
    payload: SigninEmailDto,
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
    logger.info("Signin with Email")

    entity = SigninEmailEntity(**payload.model_dump())

    use_case = SignInWithEmailUseCase(
        email_repository=EmailRepository(),
        user_repository=UserRepository(),
        login_method_repository=LoginMethodRepository(),
        refresh_token_repository=RefreshTokenRepository()
    )

    jwt, refresh_token = use_case.execute(payload=entity)

    return ResponseEntity(
        data={
            "jwt": jwt,
            "refresh_token": refresh_token
        },
        code=StatusCodes.HTTP_200_OK,
    )
