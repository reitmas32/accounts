from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from shared.databases.orms.sqlalchemy.base_model_sqlalchemy import BaseModelClass
from shared.databases.orms.sqlalchemy.models.login_methods import LoginMethodModel

from .user import UserModel


class RefreshTokenModel(BaseModelClass):

    __tablename__ = "refresh_token"

    user_id = Column(
        ForeignKey(UserModel.id ),
        nullable=False,
        index=True,
    )

    login_method_id = Column(
        ForeignKey(LoginMethodModel.id ),
        nullable=False,
        index=True,
    )

    # With this filed create de JWT
    external_id = Column(String(36), nullable=False)

    expires_at = Column(DateTime, nullable=False)

    revoked_at = Column(DateTime, nullable=True, default=None)

    user = relationship(UserModel, primaryjoin="RefreshTokenModel.user_id == UserModel.id")

    login_method = relationship(LoginMethodModel, primaryjoin="RefreshTokenModel.login_method_id == LoginMethodModel.id")
