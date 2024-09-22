from fastapi import status

from api.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from api.v1.platforms.domain.entities.singup import SignupPlatformEntity
from api.v1.platforms.domain.usecase.signup import SignUpPlatformUseCase
from api.v1.platforms.infrastructure.repositories.postgres.user import (
    PlatformRepository,
)
from api.v1.platforms.presentation.dtos.signup import SignupPlatformDto
from api.v1.platforms.presentation.endpoints.routers import router
from api.v1.users.infrastructure.repositories.postgres.user import UserRepository
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)


@router.post(
    "/signup",
    summary="Signup By Platform",
    status_code=status.HTTP_201_CREATED,
    response_model=EnvelopeResponse,
    tags=["Auth API"],
)
async def signup(
    payload: SignupPlatformDto,
):
    logger.info("Signup By Platform")

    entity: SignupPlatformEntity = SignupPlatformEntity(**payload.model_dump())

    use_case = SignUpPlatformUseCase(
        repository=PlatformRepository(),
        user_repository=UserRepository(),
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
