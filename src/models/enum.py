from enum import Enum

class AbstractEnum(Enum):
    @classmethod
    def list_values(cls):
        return [member.value for member in cls]


class UserAuthMethodEnum(AbstractEnum):
    SMS = "sms"
    GOOGLE_AUTHENTICATOR = "google_authenticator"
    EMAIL = "email"

class CodeTypeEnum(Enum):
    ACCOUNT_ACTIVATION = "account_activation"
    TWO_FACTOR = "two_factor"

class UserActivationMethodEnum(AbstractEnum):
    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
    MICROSOFT = "microsoft"
    APPLE = "apple"