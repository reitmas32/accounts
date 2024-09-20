from core.utils.logger import logger
from shared.app.enums import PlatformsLogin
from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class PlatformIDUniqueError(BaseError):
    http_code = StatusCodes.HTTP_409_CONFLICT
    internal_code = StatusCodes.APP_PLATFORM_ID_IS_ALREADY_REGISTERED

    def __init__(self, platform: PlatformsLogin, id: str) -> None:
        self.message = f"There is already a registered user with the platform:  {platform} and ID {id}"
        super().__init__(self.message)
        logger.error(self.message)
