
from api.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from shared.databases.postgres.models import LoginMethodModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class LoginMethodRepository(RepositoryPostgresBase):
    model = LoginMethodModel
    entity = LoginMethodEntity
