from fastapi import status

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
):
    logger.info("Signin By Platform")

    entity: SignupPlatformEntity = SignupPlatformEntity(**payload.model_dump())

    use_case = SignInPlatformUseCase(
        repository=PlatformRepository(),
        login_method_repository=LoginMethodRepository(),
        refresh_token_repository=RefreshTokenRepository(),
    )

    jwt, refresh_token = use_case.execute(payload=entity)

    return ResponseEntity(
        data={"jwt": jwt, "refresh_token": refresh_token},
        code=StatusCodes.HTTP_200_OK,
    )
