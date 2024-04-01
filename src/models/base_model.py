import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModelClass(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    is_removed = Column(Boolean, nullable=False, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


