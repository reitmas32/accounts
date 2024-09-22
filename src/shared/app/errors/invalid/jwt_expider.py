from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class JWTExpiredError(BaseError):
    http_code = StatusCodes.HTTP_400_BAD_REQUEST
    internal_code = StatusCodes.APP_JWT_EXPIRED

    def __init__(self) -> None:
        self.message = "The JWT expired"
        super().__init__(self.message)
        logger.error(self.message)
