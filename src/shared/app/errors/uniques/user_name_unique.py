from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class UserNameUniqueError(BaseError):
    http_code = StatusCodes.HTTP_409_CONFLICT
    internal_code = StatusCodes.APP_USER_NAME_IS_ALREADY_REGISTERED

    def __init__(self, user_name: str = "") -> None:
        self.message = f"There is already a registered user with the user_name: {user_name}"
        super().__init__(self.message)
        logger.error(self.message)
