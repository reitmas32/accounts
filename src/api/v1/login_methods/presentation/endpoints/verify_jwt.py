from fastapi import Header, status

from api.v1.login_methods.domain.usecase.verify_jwt import VerifyJWTUseCase
from core.utils.logger import logger
from core.utils.responses import (
    EnvelopeResponse,
)

from .routers import router


@router.post(
    "/verify-jwt",
    summary="Verify id JWT is valid",
    status_code=status.HTTP_200_OK,
    response_model=EnvelopeResponse,
    tags=["Auth API"],
)
async def verify_jwt(
    auth: str = Header(),
):
    logger.info("Verify JWT")

    jwt = auth.split(" ")[1]

    use_case = VerifyJWTUseCase(jwt= jwt)

    is_valid: bool = use_case.execute()

    return EnvelopeResponse(
        data=None,
        response_code=status.HTTP_200_OK,
        success=is_valid,
        message="JWT is valid",
    )
