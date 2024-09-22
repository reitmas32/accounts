from api.v1.emails.domain.entities.email import EmailEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateEmailUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: EmailEntity):
        return self.repository.add(**payload.model_dump())
