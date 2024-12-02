from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.v1.platforms.presentation.dtos.signup import SignupPlatformDto
from api.v1.platforms.presentation.endpoints.routers import router_operations as router
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.platforms.domain.entities.singup import SignupPlatformEntity
from context.v1.platforms.domain.usecase.signup import SignUpPlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity


@router.post(
    "/signup",
    summary="Signup By Platform",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseEntity,
)
async def signup(
    payload: SignupPlatformDto,
    session: Session = Depends(get_session)
):
    logger.info("Signup By Platform")

    entity: SignupPlatformEntity = SignupPlatformEntity(**payload.model_dump())

    use_case = SignUpPlatformUseCase(
        repository=PlatformRepository(session=session),
        user_repository=UserRepository(session=session),
        login_method_repository=LoginMethodRepository(session=session),
        refresh_token_repository=RefreshTokenRepository(session=session),
    )

    jwt, refresh_token = use_case.execute(payload=entity)

    return ResponseEntity(
        data={
            "jwt": jwt,
            "refresh_token": refresh_token
        },
        code=StatusCodes.HTTP_201_CREATED,
    )
