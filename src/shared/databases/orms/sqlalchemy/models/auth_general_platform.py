from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.app.enums import PlatformsLogin
from shared.databases.orms.sqlalchemy.base_model_sqlalchemy import BaseModelClass

from .user import UserModel


class AuthGeneralPlatformModel(BaseModelClass):
    """
    Model for storing authentication information from external platforms
    (Google, Apple, Facebook, etc.). This model tracks the association
    between users in the system and their external authentication providers.

    Inherits common fields and behavior from BaseModelClass.

    Attributes:
    -----------
    - `user_id`: Foreign key that links to the internal user in the system, referencing the `UserModel`.
    - `external_id`: Identifier provided by the external authentication platform (e.g., Google, Apple).
    - `email`: Optional field to store the email provided by the external platform (if available).
    - `active`: Boolean field indicating whether the authentication is currently active.
    - `type`: Enum field representing the external platform used for authentication, based on `PlatformsLogin`.
    - `user`: SQLAlchemy relationship linking the authentication record to the user.

    Relationships:
    --------------
    - `user`: Establishes a relationship with the `UserModel` to retrieve the associated user details.
    """

    __tablename__ = "auth_general_platforms"  # Specifies the table name in the database

    user_id = Column(
        ForeignKey(UserModel.id ),
        nullable=False,
        index=True,
    )
    """Foreign key to the `UserModel`, indicating which user the external authentication belongs to. Indexed for faster lookup."""

    external_id = Column(String(200), nullable=False)
    """Unique identifier provided by the external authentication provider (e.g., the ID from Google or Facebook)."""

    email = Column(String(100), nullable=True)
    """Optional email provided by the external platform (e.g., email used in Google or Apple account)."""

    active = Column(Boolean, nullable=False)
    """Boolean field that indicates whether this external authentication is currently active."""

    platform = Column(Enum(PlatformsLogin), nullable=False)
    """Enum field that represents the external platform (Google, Apple, Facebook, etc.). Must be one of the values defined in `PlatformsLogin`."""

    user = relationship(
        UserModel, primaryjoin="AuthGeneralPlatformModel.user_id == UserModel.id"
    )
    """SQLAlchemy relationship to the `UserModel`, allowing access to user details related to this authentication record."""
