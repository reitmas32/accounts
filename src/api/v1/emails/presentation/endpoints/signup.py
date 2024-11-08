from typing import TYPE_CHECKING

from fastapi import Request, status

from api.v1.emails.presentation.dtos import SignupEmailDto
from api.v1.emails.presentation.schemas.signup import SignupEmailSchema
from context.v1.codes.infrastructure.repositories.postgres.user import CodeRepository
from context.v1.emails.domain.entities.signup import SignupEmailEntity
from context.v1.emails.domain.usecase.create import SignUpWithEmailUseCase
from context.v1.emails.infrastructure.repositories.postgres.email import EmailRepository
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router

if TYPE_CHECKING:
    from context.v1.emails.domain.entities.email import EmailEntity


@router.post(
    "/signup",
    summary="SignUp user with email",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["Auth API"],
)
async def signup(
    request: Request,
    payload: SignupEmailDto,
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
    logger.info("Create Email")

    entity = SignupEmailEntity(**payload.model_dump())

    use_case = SignUpWithEmailUseCase(
        email_repository=EmailRepository(),
        user_repository=UserRepository(),
        code_repository=CodeRepository(),
        login_method_repository=LoginMethodRepository(),
        user_name=payload.user_name,
    )

    new_entity: EmailEntity = use_case.execute(payload=entity)

    response = SignupEmailSchema(**new_entity.model_dump())

    return EnvelopeResponse(
        data=response.model_dump(),
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
