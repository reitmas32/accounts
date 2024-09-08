from enum import StrEnum

from shared.app.repositories.email.send import SendEmailRepository


class EmailClientWrapper:

    def __init__(self, tag: str, repository: SendEmailRepository):
        self.tag = tag
        self.repository = repository

class EmailClientsEnum(StrEnum):
    """
    Enum class for managing different email sender implementations.

    This enum class provides options for selecting different email sender implementations, such as Gmail or Zoho.

    Enum Values:
        GMAIL_SENDER: Gmail email sender implementation.
        ZOHO_SENDER: Zoho email sender implementation.
    """

    GMAIL = "gmail"
    ZOHO = "zoho"

    @staticmethod
    def get_from_str(value_str: str):
        for enum_value in EmailClientsEnum:
            if enum_value.repository.tag == value_str:
                return enum_value
        raise ValueError("Invalid value for EmailClientsEnum")
