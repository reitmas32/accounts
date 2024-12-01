from context.v1.roles.domain.entities.role import RoleEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateRoleUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: RoleEntity):
        return self.repository.add(**payload.model_dump())
