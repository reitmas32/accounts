from uuid import UUID

from pydantic import BaseModel


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
