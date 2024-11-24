from sqlalchemy import Column, String

from shared.databases.orms.sqlalchemy.base_model_sqlalchemy import BaseModelClass


class RoleModel(BaseModelClass):
    __tablename__ = "roles"

    name = Column(String(20), nullable=False)

    description = Column(String(254), nullable=False)
