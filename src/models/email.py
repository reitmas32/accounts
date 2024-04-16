from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModelClass

from .user import UserModel


class EmailModel(BaseModelClass):
    __tablename__ = "emails"
    user_id = Column(ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    user = relationship(UserModel, primaryjoin="EmailModel.user_id == UserModel.id")
