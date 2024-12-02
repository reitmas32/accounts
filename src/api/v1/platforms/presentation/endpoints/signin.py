from fastapi import status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from api.v1.platforms.presentation.dtos.signin import SigninPlatformDto
from api.v1.platforms.presentation.endpoints.routers import router_operations as router
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.platforms.domain.entities.singup import SignupPlatformEntity
from context.v1.platforms.domain.usecase.singin import SignInPlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity


@router.post(
    "/signin",
    summary="Signin By Platform",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def signip(
    payload: SigninPlatformDto,
    session: Session = Depends(get_session)

):
    logger.info("Signin By Platform")

    entity: SignupPlatformEntity = SignupPlatformEntity(**payload.model_dump())

    use_case = SignInPlatformUseCase(
        repository=PlatformRepository(session=session),
        login_method_repository=LoginMethodRepository(session=session),
        refresh_token_repository=RefreshTokenRepository(session=session),
    )

    jwt, refresh_token = use_case.execute(payload=entity)

    return ResponseEntity(
        data={"jwt": jwt, "refresh_token": refresh_token},
        code=StatusCodes.HTTP_200_OK,
    )
