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


class NotAuthorizationException(BaseAppException):
    error_key = "NotAuthorization"
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(self, message: str = "Not autorization", resource: str | None = None) -> None:
        self.resource = resource
        self.message = f"{message} to resorce {resource}"
        logger.error(self.message)

    def to_dict(self):
        return {"endpoint": f"Dont autorization to resource {self.resource}"}

    def __str__(self):
        return f"Dont autorization to resource {self.resource}"


class EncryptedException(BaseAppException):
    error_key = "Encrypted"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str = "Not encrypted exception") -> None:
        self.message = message
        logger.error(self.message)

    def to_dict(self):
        return {"encrypted": self.message}

    def __str__(self):
        return f"Encrypted error {self.message}"

class ServiceNameException(BaseAppException):
    error_key = "ServiceName"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str = "The service name is already in use") -> None:
        self.message = message
        logger.error(self.message)

    def to_dict(self):
        return {"service_name": self.message}

    def __str__(self):
        return f"ServiceName error {self.message}"

class EmailUniqueException(BaseAppException):
    error_key = "EmailUnique"
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str = "There is already a registered user with the email: ", email: str = "") -> None:
        self.message = f"{message} {email}"
        logger.error(self.message)

    def to_dict(self):
        return {"email": self.message}

    def __str__(self):
        return self.message

class UserNameUniqueException(BaseAppException):
    error_key = "EmailUnique"
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str = "There is already a registered user with the user_name: ", user_name: str = "") -> None:
        self.message = f"{message} {user_name}"
        logger.error(self.message)

    def to_dict(self):
        return {"email": self.message}

    def __str__(self):
        return self.message

class DontFindResourceException(BaseAppException):
    error_key = "DontFindResoruce"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "The resource dont find: ", resource: str = "") -> None:
        self.message = f"{message} {resource}"
        logger.error(self.message)

    def to_dict(self):
        return {"resource": self.message}

    def __str__(self):
        return self.message

class DontValidCodeException(BaseAppException):
    error_key = "DontValidCode"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "The code is dont valid ", code: str = "", user_name: str = "") -> None:
        self.message = f"{message} code :{code} user_name: {user_name}"
        logger.error(self.message)

    def to_dict(self):
        return {"resource": self.message}

    def __str__(self):
        return self.message

class CodeAlreadyExpiredException(BaseAppException):
    error_key = "CodeAlreadyExpired"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "The code has already expired ", code: str = "", user_name: str = "") -> None:
        self.message = f"{message} code: {code} user_name: {user_name}"
        logger.error(self.message)

    def to_dict(self):
        return {"resource": self.message}

    def __str__(self):
        return self.message

class CodeAlreadyUseException(BaseAppException):
    error_key = "CodeAlreadyUse"
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, message: str = "The code has already used ", code: str = "", user_name: str = "") -> None:
        self.message = f"{message} code :{code} user_name: {user_name}"
        logger.error(self.message)

    def to_dict(self):
        return {"resource": self.message}

    def __str__(self):
        return self.message
class PasswordNoneException(BaseAppException):
    error_key = "PasswordNone"
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str = "The password cannot be None") -> None:
        self.message = message
        logger.error(self.message)

    def to_dict(self):
        return {"password": self.message}

    def __str__(self):
        return self.message

class PasswordNotValidException(BaseAppException):
    error_key = "PasswordNotValid"
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str = "The password must have [A-Za-z0-9 &%$*?¿¡!]") -> None:
        self.message = message
        logger.error(self.message)

    def to_dict(self):
        return {"password": self.message}

    def __str__(self):
        return self.message

class StepSAGAException(BaseAppException):
    error_key = "StepSAGA"
    status_code = status.HTTP_409_CONFLICT

    def __init__(self, message: str = "Error in Step") -> None:
        self.message = f"{message}"
        logger.error(self.message)

    def to_dict(self):
        return {"step": self.message}

    def __str__(self):
        return self.message
