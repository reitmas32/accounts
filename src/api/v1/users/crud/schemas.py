from datetime import date
from uuid import UUID

from pydantic import BaseModel

from core.utils.schema_base import BaseSchema


class ListUserSchema(BaseModel):
    """
    Schema for listing user data.

    This schema defines the structure for listing user data, including the user ID and username.

    Args:
        BaseModel: Base class for Pydantic models.

    Attributes:
        id (UUID): Unique identifier for the user.
        user_name (str): Username of the user.
    """

    id: UUID
    user_name: str


class UserSchema(BaseModel):
    """
    Schema for user data.

    This schema defines the structure for user data, including username, name, birthday, and optional extra data.

    Args:
        BaseModel: Base class for Pydantic models.

    Attributes:
        user_name (str): Username of the user.
        name (str, optional): Name of the user, defaults to None.
        birthday (date, optional): Birthday of the user, defaults to None.
        extra_data (dict, optional): Additional data associated with the user, defaults to None.
    """

    user_name: str
    name: str | None = None
    birthday: date | None = None
    extra_data: dict | None = None


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
    extra_data: dict | None = None


class CreateUserSchema(UserSchema):
    pass
