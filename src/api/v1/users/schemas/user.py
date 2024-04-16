from datetime import date

from pydantic import BaseModel


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
