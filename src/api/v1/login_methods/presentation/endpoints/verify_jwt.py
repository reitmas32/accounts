from fastapi import Header, status

from context.v1.login_methods.domain.usecase.verify_jwt import VerifyJWTUseCase
from core.utils.logger import logger
from shared.app.status_code import StatusCodes
from shared.presentation.schemas.envelope_response import ResponseEntity

from .routers import router_verify as router


@router.get(
    "/verify-jwt",
    summary="Verify id JWT is valid",
    status_code=status.HTTP_200_OK,
    response_model=ResponseEntity,
)
async def verify_jwt(
    auth: str = Header(),
):
    logger.info("Verify JWT")

    jwt = auth.split(" ")[1]

    use_case = VerifyJWTUseCase(jwt=jwt)

    is_valid: bool = use_case.execute()

    response = {"message": "JWT is valid", "is_valid": is_valid}

    return ResponseEntity(data=response, code=StatusCodes.HTTP_200_OK)
