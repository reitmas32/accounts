from enum import Enum


class AbstractEnum(Enum):
    @classmethod
    def list_values(cls):
        return [member.value for member in cls]

class AuthGeneralPlatformsEnum(AbstractEnum):
    FACEBOOK = "facebook"
    GOOGLE = "google"
    APPLE = "apple"

class UserActivationMethodEnum(AbstractEnum):
    FACEBOOK = "facebook"
    GOOGLE = "google"
    APPLE = "apple"
    EMAIL = "email"

class UserLoginMethodsTypeEnum(AbstractEnum):
    AUTH_GENERAL_PLATFORMS = "auth_general_platforms"
    AUTH_EMAIL = "auth_email"

    def get_type(specific_method:UserActivationMethodEnum):
        if specific_method == UserActivationMethodEnum.EMAIL:
            return UserLoginMethodsTypeEnum.AUTH_EMAIL
        return UserLoginMethodsTypeEnum.AUTH_GENERAL_PLATFORMS

class UserAuthMethodEnum(AbstractEnum):
    SMS = "sms"
    GOOGLE_AUTHENTICATOR = "google_authenticator"
    EMAIL = "email"

class CodeTypeEnum(Enum):
    ACCOUNT_ACTIVATION = "account_activation"
    TWO_FACTOR = "two_factor"
