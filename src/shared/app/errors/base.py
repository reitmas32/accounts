from core.utils.logger import logger
from shared.app.status_code import StatusCodes


class BaseError(Exception):
    error_key = None
    external_code = StatusCodes.HTTP_400_BAD_REQUEST
    internal_code = StatusCodes.HTTP_400_BAD_REQUEST

    def __init__(self, message):
        super().__init__(message)
        # If error_key isn't defined, use the class name
        self.error_name = self.error_key or self.__class__.__name__
        self.message = message
        logger.warning(self.to_dict().__str__())

    def to_dict(self):
        return {self.error_name: str(self.message)}

    def __str__(self):
        return str(self.to_dict())

