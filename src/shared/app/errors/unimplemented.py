from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class UnimplementedError(BaseError):
    external_code = StatusCodes.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code = StatusCodes.APP_UNIMPLEMENTED_ERROR

    def __init__(self, resource: str) -> None:
        self.message = f"The resource: {resource} is not implemented yet"
        super().__init__(self.message)
        logger.error(self.message)
