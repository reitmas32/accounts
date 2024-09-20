from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class PasswordError(BaseError):
    external_code = StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY
    internal_code = StatusCodes.APP_INVALID_PASSWORD_FORMAT

    def __init__(self) -> None:
        self.message = "The password must have [A-Za-z0-9 &%$*?¿¡!]"
        super().__init__(self.message)
        logger.error(self.message)
