from uuid import UUID

from shared.databases.infrastructure.repository import RepositoryInterface


class RetriveRoleUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, id: UUID):
        return self.repository.get_by_id(id)
