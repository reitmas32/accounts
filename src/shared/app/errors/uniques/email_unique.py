from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class EmailUniqueError(BaseError):
    http_code = StatusCodes.HTTP_409_CONFLICT
    internal_code = StatusCodes.APP_EMAIL_IS_ALREADY_REGISTERED

    def __init__(self, email: str) -> None:
        self.message = f"There is already a registered user with the email:  {email}"
        super().__init__(self.message)
        logger.error(self.message)

