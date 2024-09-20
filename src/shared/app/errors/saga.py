from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class SAGAError(BaseError):
    external_code = StatusCodes.HTTP_400_BAD_REQUEST
    internal_code = StatusCodes.APP_STEPS_ERROR

    def __init__(self, message: str = "Error in SAGA") -> None:
        self.message = message
        super().__init__(self.message)
        logger.error(self.message)
