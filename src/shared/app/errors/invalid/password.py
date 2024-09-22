from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class PasswordError(BaseError):
    external_code = StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY
    internal_code = StatusCodes.APP_INVALID_PASSWORD_FORMAT

    def __init__(self, message: str = "The password must have", value: str = "[A-Za-z0-9 &%$*?¿¡!]") -> None:
        self.message = f"{message} {value}"
        super().__init__(self.message)
        logger.error(self.message)
