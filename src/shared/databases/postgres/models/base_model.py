import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModelClass(Base):
    """
    Abstract base class for ORM models in SQLAlchemy that defines some common
    fields and behaviors. This class extends SQLAlchemy's `Base` and a custom
    `QueryModel`. Models inheriting from this class will use the 'accounts' schema by default.

    Attributes:
    -----------
    - `id`: A unique identifier (UUID) generated automatically, serving as the primary key.
    - `created`: Timestamp of when the record was created, with the current date as the default value.
    - `updated`: Timestamp of when the record was last updated, automatically updated on every modification.
    - `is_removed`: Indicates whether the record has been "removed" (soft delete), a boolean field with a default value of `False`.

    Methods:
    --------
    - `as_dict()`: Converts a model instance into a dictionary where each key is
      the name of the column and the value is the current value of that column.
    """

    __abstract__ = True
    __table_args__ = {"schema": "accounts"}  # noqa: RUF012

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    """UUID column serving as the primary key. A new UUID is automatically generated when creating a new record."""

    created = Column(DateTime, default=datetime.datetime.utcnow)
    """DateTime column that stores the creation timestamp of the record. The default value is the current time."""

    updated = Column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )
    """DateTime column that stores the timestamp of the last update. It automatically updates on every modification."""

    is_removed = Column(Boolean, nullable=False, default=False)
    """Boolean column that indicates whether the record has been removed. It is used to implement soft deletes."""

    def as_dict(self):
        """
        Converts the model instance into a dictionary where the keys are
        column names and the values are the current values of each column.

        Returns:
        --------
        dict: A dictionary containing the model's data.
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
