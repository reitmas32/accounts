from collections.abc import Generator

import sentry_sdk
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from core.settings import log, settings
from core.utils.exceptions import BaseAppException
from models import (
    AuthGeneralPlatformModel,
    CodeModel,
    EmailModel,
    LoginMethodModel,
    UserModel,
)
from models.base_model import Base as BaseModel

engine = create_engine(
    settings.POSTGRES_DSN.unicode_string(),
    poolclass=NullPool,
    connect_args={"application_name": "fee-api-service"},
)
Session = sessionmaker(bind=engine, autocommit=False)  # noqa: F811


def get_session() -> Generator:
    log.info("Getting db session")
    db = Session()
    log.info("DB session has been stablished")
    try:
        yield db
    except Exception as exc:  # noqa: BLE001
        db.rollback()
        sentry_sdk.capture_exception(exc)
        log.info(exc)
    finally:
        db.close()


def create_schemas():
    schema_format = "CREATE SCHEMA IF NOT EXISTS {}"
    query_schema_public = text(schema_format.format("public"))
    query_schema_accounts = text(schema_format.format("accounts"))

    with engine.connect() as conn:
        with conn.begin():
            conn.execute(query_schema_public)
            conn.execute(query_schema_accounts)

        conn.close()


class DatabaseSessionMixin:
    """Database session mixin."""

    def __enter__(self) -> Session:  # type: ignore  # noqa: PGH003
        self.session = next(get_session())
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


def use_database_session():
    return DatabaseSessionMixin()


def validate_db_conections():
    try:
        session = next(get_session())
        session.execute(select(UserModel).select_from(UserModel).limit(1)).all()
        log.info("1) Table 'users'................. O.K")
        session.execute(select(CodeModel).select_from(CodeModel).limit(1)).all()
        log.info("2) Table 'codes'................. O.K")
        session.execute(select(LoginMethodModel).select_from(LoginMethodModel).limit(1)).all()
        log.info("3) Table 'user_login_methods'..... O.K")
        session.execute(select(EmailModel).select_from(EmailModel).limit(1)).all()
        log.info("4) Table 'auth_email'..... O.K")
        session.execute(select(AuthGeneralPlatformModel).select_from(AuthGeneralPlatformModel).limit(1)).all()
        log.info("5) Table 'auth_general_platform'..... O.K")
        log.info("Connection 💲 Success")
    except Exception as e:  # noqa: BLE001
        session.close()
        message_error = f"Error on validate_db_conections, message error: {e}"
        raise BaseAppException(message_error)


def init_db():
    create_schemas()
    BaseModel.metadata.create_all(engine)
