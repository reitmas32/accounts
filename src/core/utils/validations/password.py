import re
from enum import Enum
from typing import Any

from core.settings import settings
from shared.app.errors.invalid.password import PasswordError


class ValidationEntity:
    name: str
    validation_fn: Any
    error: Exception

    def __init__(self, name: str, validation_fn, error: Exception):
        self.name = name
        self.validation_fn = validation_fn
        self.error = error


class PasswordValidation(Enum):
    MIN_LENGTH = ValidationEntity(
        name="min_length",
        validation_fn=lambda value: len(value) >= settings.PASSWORD_MIN_LENGTH,
        error=PasswordError(
            message="Password min_length", value=str(settings.PASSWORD_MIN_LENGTH)
        ),
    )
    MAX_LENGTH = ValidationEntity(
        name="max_length",
        validation_fn=lambda value: len(value) <= settings.PASSWORD_MAX_LENGTH,
        error=PasswordError(
            message="Password max_length", value=str(settings.PASSWORD_MAX_LENGTH)
        ),
    )
    UPPERCASE = ValidationEntity(
        name="uppercase",
        validation_fn=lambda value: len(re.findall(r"[A-Z]", value))
        >= settings.PASSWORD_UPPERCASE_COUNT,
        error=PasswordError(
            message="Password uppercase_count", value=str(settings.PASSWORD_UPPERCASE_COUNT)
        ),
    )
    LOWERCASE = ValidationEntity(
        name="lowercase",
        validation_fn=lambda value: len(re.findall(r"[a-z]", value))
        >= settings.PASSWORD_LOWERCASE_COUNT,
        error=PasswordError(
            message="Password lowercase_count", value=str(settings.PASSWORD_LOWERCASE_COUNT)
        ),
    )
    DIGIT = ValidationEntity(
        name="digit",
        validation_fn=lambda value: len(re.findall(r"[0-9]", value))
        >= settings.PASSWORD_DIGIT_COUNT,
        error=PasswordError(
            message="Password digit_count", value=str(settings.PASSWORD_DIGIT_COUNT)
        ),
    )
    SPECIAL_CHAR = ValidationEntity(
        name="special_char",
        validation_fn=lambda value: len(
            re.findall(re.compile(settings.PASSWORD_SPECIAL_CHARS), value)
        )
        >= settings.PASSWORD_SPECIAL_CHAR_COUNT,
        error=PasswordError(
            message=f"Password special_char_count {settings.PASSWORD_SPECIAL_CHARS}", value=str(settings.PASSWORD_SPECIAL_CHAR_COUNT)
        ),
    )


active_validations: list[PasswordValidation] = [
    getattr(PasswordValidation, name) for name in settings.PASSWORD_VALIDATIONS
]
