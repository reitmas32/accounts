
from context.v1.codes.domain.entities.code import CodeEntity
from shared.databases.orms.sqlalchemy.models import CodeModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class CodeRepository(RepositoryPostgresBase):
    model = CodeModel
    entity = CodeEntity
