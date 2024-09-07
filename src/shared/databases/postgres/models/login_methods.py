from sqlalchemy import Boolean, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.app.enums import UserLoginMethodsTypeEnum
from shared.databases.postgres.models.base_model import BaseModelClass
from shared.databases.postgres.models.user import UserModel


class LoginMethodModel(BaseModelClass):
    """
    Model for storing login methods associated with a user. This model tracks different
    authentication methods (e.g., email, phone number) that a user can use to log into the system.

    Inherits common fields and behavior from BaseModelClass.

    Attributes:
    -----------
    - `user_id`: Foreign key linking the login method to the corresponding user in the `UserModel`.
    - `entity_id`: UUID representing the unique identifier for the entity (e.g., device or account) tied to the login method.
    - `entity_type`: Enum field specifying the type of login method (email, phone, etc.) using `UserLoginMethodsTypeEnum`.
    - `active`: Boolean flag indicating whether the login method is active for the user.
    - `verify`: Boolean flag indicating whether the login method has been verified (e.g., email or phone confirmation).

    Relationships:
    --------------
    - `user`: Establishes a relationship with the `UserModel`, linking the login method to the user.
    """

    __tablename__ = "login_methods"  # Specifies the table name in the database

    user_id = Column(
        ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"),
        nullable=False,
        index=True,
    )
    """Foreign key to the `UserModel`, indicating which user the login method belongs to. Indexed for faster lookup."""

    entity_id = Column(UUID, nullable=False)
    """UUID representing the entity associated with the login method (e.g., device or account)."""

    entity_type = Column(Enum(UserLoginMethodsTypeEnum), nullable=False)
    """Enum field representing the type of login method, such as email or phone number, based on `UserLoginMethodsTypeEnum`."""

    active = Column(Boolean, nullable=False, default=False)
    """Boolean flag indicating whether the login method is currently active."""

    verify = Column(Boolean, nullable=False, default=False)
    """Boolean flag indicating whether the login method has been verified (e.g., email or phone confirmation)."""

    user = relationship(
        UserModel, primaryjoin="LoginMethodModel.user_id == UserModel.id"
    )
    """SQLAlchemy relationship to the `UserModel`, allowing access to user details related to this login method."""
