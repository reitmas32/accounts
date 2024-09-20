from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class AccountUnverifiedError(BaseError):
    external_code = StatusCodes.HTTP_401_UNAUTHORIZED
    internal_code = StatusCodes.APP_ALREADY_USED_CODE

    def __init__(self) -> None:
        self.message = "The account is not verified"
        super().__init__(self.message)
        logger.error(self.message)
