
from context.v1.roles.domain.entities.role import RoleEntity
from shared.databases.orms.sqlalchemy.models.role import RoleModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class RoleRepository(RepositoryPostgresBase):
    model = RoleModel
    entity = RoleEntity
