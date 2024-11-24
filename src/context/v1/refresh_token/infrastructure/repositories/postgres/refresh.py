
from context.v1.refresh_token.domain.entities.refresh_token import RefreshTokenEntity
from shared.databases.orms.sqlalchemy.models import RefreshTokenModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class RefreshTokenRepository(RepositoryPostgresBase):
    model = RefreshTokenModel
    entity = RefreshTokenEntity
