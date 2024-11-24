from context.v1.refresh_token.domain.entities.refresh_token import RefreshTokenEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateRefreshTokenUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: RefreshTokenEntity):
        return self.repository.add(**payload.model_dump())
