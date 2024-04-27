from sqlalchemy import Boolean, Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base_model import BaseModelClass
from models.enum import UserLoginMethodsTypeEnum
from models.user import UserModel


class LoginMethodModel(BaseModelClass):
    __tablename__ = "login_methods"
    user_id = Column(ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    entity_id = Column(UUID, nullable=False)
    entity_type = Column(Enum(UserLoginMethodsTypeEnum), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    verify = Column(Boolean, nullable=False, default=False)

    user = relationship(UserModel, primaryjoin="LoginMethodModel.user_id == UserModel.id")
