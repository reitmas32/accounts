from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModelClass
from models.enum import AuthGeneralPlatformsEnum

from .user import UserModel


class AuthGeneralPlatformModel(BaseModelClass):
    __tablename__ = "auth_general_platforms"
    user_id = Column(ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    hashed_platform_id = Column(String, nullable=False)
    email = Column(String, nullable=True)
    active = Column(Boolean, nullable=False)
    type = Column(Enum(AuthGeneralPlatformsEnum), nullable=False)
    user = relationship(UserModel, primaryjoin="AuthGeneralPlatformModel.user_id == UserModel.id")
