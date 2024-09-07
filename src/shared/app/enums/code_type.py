from shared.app.enums.abstract import AbstractEnum


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
