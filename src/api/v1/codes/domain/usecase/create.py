from api.v1.codes.domain.entities.code import CodeEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateCodeUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: CodeEntity):
        return self.repository.add(**payload.model_dump())
