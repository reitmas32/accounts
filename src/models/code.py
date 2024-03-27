from sqlalchemy import Column, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from models.base_model import BaseModelClass
from sqlalchemy import Enum
from models.enum import CodeTypeEnum


class CodeModel(BaseModelClass):
    __tablename__ = "codes"
    code = Column(String, nullable=False)
    email = Column(String, nullable=False)
    type = Column(Enum(CodeTypeEnum), nullable=False)
    used_at = Column(DateTime, nullable=True)
