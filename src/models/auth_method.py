from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from models.base_model import BaseModelClass
from sqlalchemy import Enum
from models.enum import UserAuthMethodEnum

class UserAuthMethodModel(BaseModelClass):
    __tablename__ = "user_auth_methods"
    user_id = Column(UUID,nullable=False)
    auth_method = Column(Enum(UserAuthMethodEnum), nullable=False)