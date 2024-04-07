from sqlalchemy import JSON, Column, String

from models.base_model import BaseModelClass


class UserModel(BaseModelClass):
    __tablename__ = "users"
    user_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True, unique=True)
    extra_data = Column(JSON, nullable=True)
