
from shared.app.enums.abstract import AbstractEnum


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
