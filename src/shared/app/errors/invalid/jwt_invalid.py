from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class JWTInvalidError(BaseError):
    http_code = StatusCodes.HTTP_400_BAD_REQUEST
    internal_code = StatusCodes.APP_INVALID_DATA

    def __init__(self, message: str) -> None:
        self.message = f"The JWT is invalid: {message}"
        super().__init__(self.message)
        logger.error(self.message)
