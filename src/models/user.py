from sqlalchemy import Column, String,Boolean,JSON
from models.base_model import BaseModelClass
from sqlalchemy import Enum
from models.enum import UserAuthMethodEnum,UserActivationMethodEnum

class UserModel(BaseModelClass):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    user_name = Column(String, nullable=False)
    phone_number = Column(String,nullable=True, unique=True)
    password = Column(String, nullable=False)
    validate = Column(Boolean,nullable=False, default=False)
    activation_method = Column(Enum(UserActivationMethodEnum), nullable=True)
    auth_method_default = Column(Enum(UserAuthMethodEnum), nullable=True, default = None)
    extra_data = Column(JSON,nullable=True)