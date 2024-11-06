
from context.v1.platforms.domain.entities.platform import PlatformEntity
from shared.databases.orms.sqlalchemy.models import AuthGeneralPlatformModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class PlatformRepository(RepositoryPostgresBase):
    model = AuthGeneralPlatformModel
    entity = PlatformEntity
