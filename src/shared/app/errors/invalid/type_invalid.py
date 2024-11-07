from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class TypeInvalidError(BaseError):
    external_code = StatusCodes.HTTP_422_UNPROCESSABLE_ENTITY
    internal_code = StatusCodes.APP_INVALID_DATA

    def __init__(self, valid_type: str, invalid_type: str ) -> None:
        self.message = f"The type provider is invalid: An {invalid_type} was received but a {valid_type} was expected"
        super().__init__(self.message)
        logger.error(self.message)
