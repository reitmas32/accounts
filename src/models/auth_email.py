from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModelClass

from .user import UserModel


class AuthEmailModel(BaseModelClass):
    __tablename__ = "auth_email"
    user_id = Column(ForeignKey(UserModel.id,deferrable=True, initially="DEFERRED"),nullable=False,index=True)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    active = Column(Boolean,nullable=False)

    user = relationship(UserModel, primaryjoin="AuthEmailModel.user_id == UserModel.id")
