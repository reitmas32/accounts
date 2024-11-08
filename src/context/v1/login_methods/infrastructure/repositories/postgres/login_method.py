
from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from shared.databases.orms.sqlalchemy.models import LoginMethodModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class LoginMethodRepository(RepositoryPostgresBase):
    model = LoginMethodModel
    entity = LoginMethodEntity
