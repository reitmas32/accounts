from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def list_values(cls):
        return [member.value for member in cls]


class PlatformsLogin(str, Enum):
    FACEBOOK = "facebook"
    GOOGLE = "google"
    APPLE = "apple"

    @staticmethod
    def get_enum_from_str(value_str: str):
        for enum_value in UserAuthMethodEnum:
            if enum_value.value == value_str:
                return enum_value
        raise ValueError("Invalid value for UserAuthMethodEnum")


class UserLoginMethodsTypeEnum(AbstractEnum):
    FACEBOOK = "facebook"
    GOOGLE = "google"
    APPLE = "apple"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"

    @staticmethod
    def get_enum_from_str(value_str: str):
        for enum_value in UserLoginMethodsTypeEnum:
            if enum_value.value == value_str:
                return enum_value
        raise ValueError("Invalid value for UserLoginMethodsTypeEnum")


class UserAuthMethodEnum(AbstractEnum):
    SMS = "sms"
    GOOGLE_AUTHENTICATOR = "google_authenticator"
    EMAIL = "email"

    @staticmethod
    def get_enum_from_str(value_str: str):
        for enum_value in UserAuthMethodEnum:
            if enum_value.value == value_str:
                return enum_value
        raise ValueError("Invalid value for UserAuthMethodEnum")


class CodeTypeEnum(AbstractEnum):
    ACCOUNT_ACTIVATION = "account_activation"
    RESET_PASSWORD = "reset_password"  # noqa: S105
    TWO_FACTOR = "two_factor"

    @staticmethod
    def get_enum_from_str(value_str: str):
        for enum_value in CodeTypeEnum:
            if enum_value.value == value_str:
                return enum_value
        raise ValueError("Invalid value for CodeTypeEnum")
