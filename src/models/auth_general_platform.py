from sqlalchemy import Column,String,Boolean,ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.base_model import BaseModelClass
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from .user import UserModel
from models.enum import AuthGeneralPlatformsEnum

class AuthGeneralPlatformModel(BaseModelClass):
    __tablename__ = "auth_general_platforms"
    user_id = Column(ForeignKey(UserModel.id,deferrable=True, initially="DEFERRED"),nullable=False,index=True)
    hashed_platform_id  = Column(String,nullable=False)
    email = Column(String,nullable=True)
    active = Column(Boolean,nullable=False)
    type = Column(Enum(AuthGeneralPlatformsEnum), nullable=False)
    user = relationship(UserModel, primaryjoin="AuthGeneralPlatformModel.user_id == UserModel.id")