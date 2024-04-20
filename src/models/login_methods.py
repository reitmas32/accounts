from sqlalchemy import Boolean, Column, Enum
from sqlalchemy.dialects.postgresql import UUID

from models.base_model import BaseModelClass
from models.enum import UserLoginMethodsTypeEnum


class UserLoginMethodModel(BaseModelClass):
    __tablename__ = "user_login_methods"
    user_id = Column(UUID, nullable=False)
    entity_id = Column(UUID, nullable=False)
    entity_type = Column(Enum(UserLoginMethodsTypeEnum), nullable=False)
    active = Column(Boolean, nullable=False, default=False)
    verify = Column(Boolean, nullable=False, default=False)
