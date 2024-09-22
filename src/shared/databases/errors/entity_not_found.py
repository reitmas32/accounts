from core.utils.logger import logger
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class EntityNotFoundError(BaseError):
    http_code = StatusCodes.HTTP_404_NOT_FOUND
    internal_code = StatusCodes.APP_DONT_FOUND_ENTITY

    def __init__(self, message: str = "The resource dont find: ", resource: str = "") -> None:
        self.message = f"{message} {resource}"
        logger.error(self.message)

    def to_dict(self):
        return {"resource": self.message}

    def __str__(self):
        return self.message
