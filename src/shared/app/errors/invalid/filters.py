from shared.app.errors.base import BaseError
from shared.app.status_code import StatusCodes


class FilterError(BaseError):
    http_code = StatusCodes.HTTP_400_BAD_REQUEST
    internal_code = StatusCodes.APP_INVALID_DATA

    def __init__(self, invalid_keys: list | None = None, valid_keys: list | None = None) -> None:
        self.invalid_keys = invalid_keys
        self.valid_keys = valid_keys
        super().__init__(self.to_dict().__str__())

    def to_dict(self):
        return {value: f"Choose one of {self.valid_keys}" for value in self.invalid_keys}
