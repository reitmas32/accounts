from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from context.v1.login_methods.domain.usecase.verify_jwt import VerifyJWTUseCase
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_verify as router

security_scheme = HTTPBearer()


@router.get(
    "/verify-jwt",
    summary="Verify if JWT is valid",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
    dependencies=[Depends(security_scheme)],
)
async def verify_jwt(
    authorization: HTTPAuthorizationCredentials = Depends(security_scheme),
):
    logger.info("Verify JWT")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization header is missing",
        )

    jwt = authorization.credentials

    use_case = VerifyJWTUseCase(jwt=jwt)
    is_valid: bool = use_case.execute()

    response = {"message": "JWT is valid", "is_valid": is_valid}

    return ResponseEntity(data=response, code=StatusCodes.HTTP_200_OK)
