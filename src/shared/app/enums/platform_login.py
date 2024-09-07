from shared.app.enums.abstract import AbstractEnum


class PlatformsLogin(AbstractEnum):
    FACEBOOK = "facebook"
    GOOGLE = "google"
    APPLE = "apple"

    @staticmethod
    def get_enum_from_str(value_str: str):
        for enum_value in PlatformsLogin:
            if enum_value.value == value_str:
                return enum_value
        raise ValueError("Invalid value for UserAuthMethodEnum")
