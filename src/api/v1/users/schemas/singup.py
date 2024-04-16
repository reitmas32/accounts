import phonenumbers
from pydantic import EmailStr, validator

from core.utils.schema_base import BaseSchema

from .user import UserSchema

#################
# Requests
#################


class SignupEmailSchema(UserSchema):
    """
    Schema for email-based user signup.

    This schema extends the UserSchema and includes fields for email and password.
    It also includes a validator for phone number format.

    Args:
        UserSchema: Base schema for user-related data.

    Attributes:
        email (EmailStr): Email address of the user.
        password (str): Password for the user account.

    Methods:
        validate_phone_number: Validates the format of the phone number field.
    """

    email: EmailStr
    password: str

    @staticmethod
    @validator("phone_number", pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):  # noqa: ARG004
        """
        Validates the format of the phone number field.

        Args:
            v (str): Phone number to validate.

        Returns:
            str: Valid phone number.

        Raises:
            ValueError: If the phone number is invalid or in an invalid format.
        """
        if v is not None:
            try:
                number = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(number):
                    raise ValueError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        return v


class SignupPhoneNumberSchema(UserSchema):
    """
    Schema for phone number-based user signup.

    This schema extends the UserSchema and includes a field for the phone number.
    It also includes a validator for phone number format.

    Args:
        UserSchema: Base schema for user-related data.

    Attributes:
        phone_number (str): Phone number of the user.

    Methods:
        validate_phone_number: Validates the format of the phone number field.
    """

    phone_number: str

    @staticmethod
    @validator("phone_number", pre=True, allow_reuse=True)
    def validate_phone_number(cls, v):  # noqa: ARG004
        """
        Validates the format of the phone number field.

        Args:
            v (str): Phone number to validate.

        Returns:
            str: Valid phone number.

        Raises:
            ValueError: If the phone number is invalid or in an invalid format.
        """
        if v is not None:
            try:
                number = phonenumbers.parse(v, None)
                if not phonenumbers.is_valid_number(number):
                    raise ValueError("Invalid phone number")
            except phonenumbers.NumberParseException:
                raise ValueError("Invalid phone number format")
        return v


#################
# Responses
#################


class RetrieveSingUpEmailEmailSchema(BaseSchema):
    """
    Schema for retrieving email information during email-based user signup retrieval.

    This schema defines the structure for retrieving user name and email during email-based user signup retrieval.

    Args:
        BaseSchema: Base schema for data retrieval.

    Attributes:
        user_name (str): Username associated with the retrieved email.
        email (str): Email address retrieved during email-based user signup retrieval.
    """

    user_name: str
    email: str


class RetrieveUserSchema(BaseSchema):
    """
    Schema for retrieving user information.

    This schema defines the structure for retrieving user data, including username, phone number, email, and optional extra data.

    Args:
        BaseSchema: Base schema for data retrieval.

    Attributes:
        user_name (str): Username associated with the retrieved user information.
        phone_number (str, optional): Phone number associated with the retrieved user information, defaults to None.
        email (str, optional): Email address associated with the retrieved user information, defaults to None.
        extra_data (dict, optional): Additional data associated with the retrieved user information, defaults to None.
    """

    user_name: str
    phone_number: str | None = None
    email: str | None = None
    extra_data: dict | None = None
