from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateLoginMethodUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: LoginMethodEntity):
        return self.repository.add(**payload.model_dump())
