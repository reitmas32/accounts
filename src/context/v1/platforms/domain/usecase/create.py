from context.v1.platforms.domain.entities.platform import PlatformEntity
from shared.databases.infrastructure.repository import RepositoryInterface


class CreatePlatformUseCase:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def execute(self, payload: PlatformEntity):
        return self.repository.add(**payload.model_dump())
