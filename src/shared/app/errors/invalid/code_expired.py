from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class CodeExpiredError(BaseError):
    http_code = StatusCodes.HTTP_404_NOT_FOUND
    internal_code = StatusCodes.APP_EXPIRED_CODE

    def __init__(self, code: str, operation: str = "verify") -> None:
        self.message = f"The code: {code} expired by operation: {operation}"
        super().__init__(self.message)
        logger.error(self.message)
