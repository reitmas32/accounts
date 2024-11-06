from fastapi import status

from api.v1.platforms.presentation.dtos.signin import SigninPlatformDto
from api.v1.platforms.presentation.endpoints.routers import router
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.platforms.domain.entities.singup import SignupPlatformEntity
from context.v1.platforms.domain.usecase.singin import SignInPlatformUseCase
from context.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)


@router.post(
    "/signin",
    summary="Signin By Platform",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["Auth API"],
)
async def signup(
    payload: SigninPlatformDto,
):
    logger.info("Signin By Platform")

    entity: SignupPlatformEntity = SignupPlatformEntity(**payload.model_dump())

    use_case = SignInPlatformUseCase(
        repository=PlatformRepository(),
        login_method_repository=LoginMethodRepository(),
    )

    jwt = use_case.execute(
        payload=entity
    )  # el caso de uso debe genera una Response intermedia o porlomenos retornar el stataus code

    return EnvelopeResponse(
        data=jwt,
        success=True,
        response_code=status.HTTP_201_CREATED,
    )
