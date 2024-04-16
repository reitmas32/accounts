from sqlalchemy import JSON, Column, Date, String

from models.base_model import BaseModelClass


class UserModel(BaseModelClass):
    __tablename__ = "users"
    user_name = Column(String, nullable=False)
    name = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    extra_data = Column(JSON, nullable=True)
