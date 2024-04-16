from sqlalchemy import Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from models.base_model import BaseModelClass
from models.enum import CodeTypeEnum, UserLoginMethodsTypeEnum

from .user import UserModel


class CodeModel(BaseModelClass):
    __tablename__ = "codes"
    code = Column(String, nullable=False)
    user_id = Column(ForeignKey(UserModel.id, deferrable=True, initially="DEFERRED"), nullable=False, index=True)
    entity_id = Column(UUID, nullable=False)
    entity_type = Column(Enum(UserLoginMethodsTypeEnum), nullable=False)
    type = Column(Enum(CodeTypeEnum), nullable=False)
    used_at = Column(DateTime, nullable=True)

    user = relationship(UserModel, primaryjoin="CodeModel.user_id == UserModel.id")
