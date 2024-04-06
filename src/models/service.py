from sqlalchemy import Column, String

from models.base_model import BaseModelClass


class ServiceModel(BaseModelClass):
    __tablename__ = "services"
    api_key = Column(String, nullable=False)
    service_name = Column(String, nullable=False)
