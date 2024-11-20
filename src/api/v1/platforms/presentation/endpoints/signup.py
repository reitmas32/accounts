from fastapi import status

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
from context.v1.users.infrastructure.repositories.postgres.user import UserRepository
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
):
    logger.info("Signup By Platform")

    entity: SignupPlatformEntity = SignupPlatformEntity(**payload.model_dump())

    use_case = SignUpPlatformUseCase(
        repository=PlatformRepository(),
        user_repository=UserRepository(),
        login_method_repository=LoginMethodRepository(),
    )

    jwt = use_case.execute(payload=entity)

    return ResponseEntity(data=jwt, code=StatusCodes.HTTP_201_CREATED)
