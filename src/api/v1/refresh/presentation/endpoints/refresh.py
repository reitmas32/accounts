from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from api.v1.refresh.presentation.schemas.new_jwt import NewJWTSchema
from context.v1.login_methods.infrastructure.repositories.postgres.login_method import (
    LoginMethodRepository,
)
from context.v1.refresh_token.domain.usecase.refresh import RefreshTokenUseCase
from context.v1.refresh_token.infrastructure.repositories.postgres.refresh import (
    RefreshTokenRepository,
)
from core.settings.database import get_session
from core.utils.logger import logger
from shared.app.depends.custom_http_bearer import CustomHTTPBearer
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_operations as router

security_scheme = CustomHTTPBearer()


@router.get(
    "/refresh-jwt",
    summary="Generate a new JWT with the refresh token",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
    dependencies=[Depends(security_scheme)],
)
async def verify_jwt(
    authorization: HTTPAuthorizationCredentials = Depends(security_scheme),
    session: Session = Depends(get_session)
):
    logger.info("Verify JWT")

    jwt = authorization.credentials

    use_case = RefreshTokenUseCase(
        jwt=jwt,
        refresh_token_repository=RefreshTokenRepository(session=session),
        login_methods_repository=LoginMethodRepository(session=session),
    )
    jwt: bool = use_case.execute()

    response = NewJWTSchema(jwt=jwt)

    return ResponseEntity(data=response.model_dump(), code=StatusCodes.HTTP_200_OK)
