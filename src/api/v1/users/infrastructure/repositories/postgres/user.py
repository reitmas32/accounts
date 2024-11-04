
from api.v1.users.domain.entities.user import UserEntity
from shared.databases.orms.sqlalchemy.models.user import UserModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class UserRepository(RepositoryPostgresBase):
    model = UserModel
    entity = UserEntity
