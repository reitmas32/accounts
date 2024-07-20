from sqlalchemy import JSON, Column, Date, String, event
from sqlalchemy.orm import Session

from models.base_model import BaseModelClass


class UserModel(BaseModelClass):
    __tablename__ = "users"
    user_name = Column(String, nullable=True)
    name = Column(String, nullable=True)
    birthday = Column(Date, nullable=True)
    extra_data = Column(JSON, nullable=True)

    @staticmethod
    def generate_default_username(target, connection, **kw):  # noqa: ARG004
        if target.user_name is None:
            session = Session.object_session(target)
            count = session.query(UserModel).count() if session else 0
            target.user_name = f"User{count + 1:06}"


# Asociar el evento `before_insert` para llamar a `generate_default_username`
@event.listens_for(UserModel, "before_insert")
def set_default_username(mapper, connection, target):
    UserModel.generate_default_username(target, connection)
