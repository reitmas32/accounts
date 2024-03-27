import logging

from fastapi import status
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)


class BaseAppException(Exception):  # noqa: N818
    error_key = None  # Class variable that can be overwritten by subclasses
    status_code = status.HTTP_400_BAD_REQUEST

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


class ObjectNotFound(NoResultFound):
    def __init__(self, message, data=None):
        super().__init__(message)
        self.data = data if data is not None else {}
        logger.warning(self.__class__.__str__())


class FormException(BaseAppException):
    error_key = "FormError"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, field_errors: dict | None = None) -> None:
        self.field_errors = field_errors or {}
        logger.warning(self.to_dict().__str__())

    def to_dict(self):
        return {error: value for error, value in self.field_errors.items() if value}


class FilterException(BaseAppException):
    error_key = "FiltersError"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, invalid_keys: list | None = None, valid_keys: list | None = None) -> None:
        self.invalid_keys = invalid_keys
        self.valid_keys = valid_keys
        logger.warning(self.to_dict().__str__())

    def to_dict(self):
        return {value: f"Choose one of {self.valid_keys}" for value in self.invalid_keys}


class NotFoundObjectException(BaseAppException):
    error_key = "NotFoundObjectError"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, model_name: str | None = None, id: str | None = None) -> None:
        self.model_name = model_name
        self.id = id

    def to_dict(self):
        return {"id": f"{self.model_name} Not Found with id {self.id}"}


class NotFoundContractException(BaseAppException):
    error_key = "NotFoundContractError"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, id: str | None = None) -> None:
        self.id = id
        logger.warning(self.to_dict().__str__())

    def to_dict(self):
        return {"contract_id": f"Contract Not Found with id {self.id}"}


class FeeNotFoundException(BaseAppException):
    error_key = "FeeNotFound"
    status_code = status.HTTP_404_NOT_FOUND


class InvalidFeeTypeException(BaseAppException):
    error_key = "InvalidFeeType"


class InvalidContractException(BaseAppException):
    error_key = "InvalidContract"


class DisbursementMismatchException(BaseAppException):
    error_key = "DisbursementMismatch"


class FeeAlreadyExistsException(BaseAppException):
    error_key = "FeeAlreadyExists"
