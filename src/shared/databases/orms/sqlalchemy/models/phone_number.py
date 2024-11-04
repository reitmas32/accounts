from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.databases.orms.sqlalchemy.base_model_sqlalchemy import BaseModelClass

from .user import UserModel


class PhoneNumberModel(BaseModelClass):
    """
    Model for storing phone numbers associated with a user. This class allows the system
    to manage phone numbers linked to specific users in the `UserModel`.

    Inherits common fields and behavior from BaseModelClass.

    Attributes:
    -----------
    - `user_id`: Foreign key linking the phone number to the corresponding user in the `UserModel`.
    - `phone_number`: String representing the user's phone number.

    Relationships:
    --------------
    - `user`: Establishes a relationship with the `UserModel`, linking the phone number to the user.
    """

    __tablename__ = "phone_number"  # Specifies the table name in the database

    user_id = Column(
        ForeignKey(UserModel.id ),
        nullable=False,
        index=True,
    )
    """Foreign key to the `UserModel`, indicating which user this phone number belongs to. Indexed for faster lookup."""

    phone_number = Column(String(20), nullable=False)
    """String representing the user's phone number. This field cannot be null."""

    user = relationship(
        UserModel, primaryjoin="PhoneNumberModel.user_id == UserModel.id"
    )
    """SQLAlchemy relationship to the `UserModel`, allowing access to user details related to this phone number."""
