from api.v1.users.domain.entities.user import UserEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateUserUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: UserEntity):
        return self.repository.add(**payload.model_dump())
