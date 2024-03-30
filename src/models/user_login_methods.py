from sqlalchemy import Column,String,Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.base_model import BaseModelClass
from sqlalchemy import Enum
from models.enum import UserLoginMethodsTypeEnum

class UserLoginMethodModel(BaseModelClass):
    __tablename__ = "user_login_methods"
    user_id = Column(UUID,nullable=False)
    entity_id = Column(UUID,nullable=False)
    entity_type = Column(Enum(UserLoginMethodsTypeEnum), nullable=False)