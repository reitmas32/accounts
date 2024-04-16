from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models.base_model import BaseModelClass

from .user import UserModel


class PhoneNumberModel(BaseModelClass):
    __tablename__ = "phone_number"
    user_id = Column(ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    phone_number = Column(String, nullable=False)

    user = relationship(UserModel, primaryjoin="PhoneNumberModel.user_id == UserModel.id")
