from shared.app.enums.abstract import AbstractEnum


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
