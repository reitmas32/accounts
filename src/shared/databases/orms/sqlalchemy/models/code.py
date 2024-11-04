from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.app.enums import CodeTypeEnum, UserLoginMethodsTypeEnum
from shared.databases.orms.sqlalchemy.base_model_sqlalchemy import BaseModelClass

from .user import UserModel


class CodeModel(BaseModelClass):
    """
    Model for storing verification codes. This model tracks codes generated for users,
    which can be used for various purposes such as password resets, two-factor authentication,
    or email verification.

    Inherits common fields and behavior from BaseModelClass.

    Attributes:
    -----------
    - `code`: The actual verification code (string).
    - `user_id`: Foreign key linking the code to the user it was generated for, referencing the `UserModel`.
    - `entity_id`: UUID representing the entity (e.g., device or session) associated with the code.
    - `entity_type`: Enum field that specifies the login method or entity type, using `UserLoginMethodsTypeEnum`.
    - `type`: Enum field representing the type of code (e.g., verification, reset password), based on `CodeTypeEnum`.
    - `used_at`: Timestamp that records when the code was used, if applicable.

    Relationships:
    --------------
    - `user`: Establishes a relationship with the `UserModel`, linking the code to the corresponding user.
    """

    __tablename__ = "codes"  # Specifies the table name in the database

    code = Column(String(20), nullable=False)
    """String representing the actual verification code."""

    user_id = Column(
        ForeignKey(UserModel.id ),
        nullable=False,
        index=True,
    )
    """Foreign key to the `UserModel`, indicating which user the verification code was generated for. Indexed for faster lookup."""

    entity_id = Column(String(36), nullable=False)
    """UUID representing the entity associated with the verification code (e.g., device or session)."""

    entity_type = Column(Enum(UserLoginMethodsTypeEnum), nullable=False)
    """Enum field representing the type of entity (e.g., email, phone, or other login methods) based on `UserLoginMethodsTypeEnum`."""

    type = Column(Enum(CodeTypeEnum), nullable=False)
    """Enum field representing the type of code, such as verification or password reset, based on `CodeTypeEnum`."""

    used_at = Column(DateTime, nullable=True)
    """Timestamp that stores the date and time when the code was used. It remains null if the code hasn't been used."""

    user = relationship(UserModel, primaryjoin="CodeModel.user_id == UserModel.id")
    """SQLAlchemy relationship to the `UserModel`, allowing access to user details related to this verification code."""
