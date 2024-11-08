
from context.v1.emails.domain.entities.email import EmailEntity
from shared.databases.orms.sqlalchemy.models import EmailModel
from shared.databases.postgres.repository import RepositoryPostgresBase


class EmailRepository(RepositoryPostgresBase):
    model = EmailModel
    entity = EmailEntity
