from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.databases.orms.sqlalchemy.base_model_sqlalchemy import BaseModelClass

from .user import UserModel


class EmailModel(BaseModelClass):
    """
    Model for storing email information linked to a user. This class stores a user's email
    and its associated password, allowing the system to track email accounts and their
    relationship to users.

    Inherits common fields and behavior from BaseModelClass.

    Attributes:
    -----------
    - `user_id`: Foreign key linking the email record to the corresponding user in the `UserModel`.
    - `email`: The email address (string) associated with the user.
    - `password`: The password linked to the email account (string).

    Relationships:
    --------------
    - `user`: Establishes a relationship with the `UserModel`, linking the email to the user.
    """

    __tablename__ = "emails"  # Specifies the table name in the database

    user_id = Column(
        ForeignKey(UserModel.id ),
        nullable=False,
        index=True,
    )
    """Foreign key to the `UserModel`, indicating which user this email belongs to. Indexed for faster lookup."""

    email = Column(String(100), nullable=False)
    """String representing the email address associated with the user. This field cannot be null."""

    password = Column(String(100), nullable=False)
    """String representing the password linked to the email account. This field cannot be null."""

    user = relationship(UserModel, primaryjoin="EmailModel.user_id == UserModel.id")
    """SQLAlchemy relationship to the `UserModel`, allowing access to user details related to this email."""
