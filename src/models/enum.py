from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def list_values(cls):
        return [member.value for member in cls]


class UserLoginMethodsTypeEnum(AbstractEnum):
    FACEBOOK = "facebook"
    GOOGLE = "google"
    APPLE = "apple"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"


class UserAuthMethodEnum(AbstractEnum):
    SMS = "sms"
    GOOGLE_AUTHENTICATOR = "google_authenticator"
    EMAIL = "email"


class CodeTypeEnum(AbstractEnum):
    ACCOUNT_ACTIVATION = "account_activation"
    TWO_FACTOR = "two_factor"
