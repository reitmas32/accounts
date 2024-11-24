from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials

from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.refresh_token.domain.usecase.refresh import RefreshTokenUseCase
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.utils.logger import logger
from shared.app.depends.custom_http_bearer import CustomHTTPBearer
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_operations as router

security_scheme = CustomHTTPBearer()


@router.get(
    "/refresh-token/jwt",
    summary="Generate a new JWT with the refresh token",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
    dependencies=[Depends(security_scheme)],
)
async def verify_jwt(
    authorization: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    logger.info("Verify JWT")

    jwt = authorization.credentials

    use_case = RefreshTokenUseCase(
        jwt=jwt,
        refresh_token_repository=RefreshTokenRepository(),
        login_methods_repository=LoginMethodRepository(),
    )
    is_valid: bool = use_case.execute()

    response = {"jwt": is_valid}

    return ResponseEntity(data=response, code=StatusCodes.HTTP_200_OK)
