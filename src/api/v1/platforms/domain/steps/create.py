from api.v1.platforms.domain.entities.platform import PlatformEntity
from api.v1.users.domain.steps.create import CreateUserByUserNameStep
from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.infrastructure.repository import RepositoryInterface


class CreatePlatformStep(StepSAGA):
    def __init__(self, entity: PlatformEntity, repository: RepositoryInterface):
        self.entity = entity
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        user = all_payloads[CreateUserByUserNameStep]
        self.entity.user_id = user.id
        self.platform = None
        self.platform = self.repository.add( **self.entity.model_dump())
        return self.platform

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        if self.platform is not None:
            self.repository.delete_by_id(self.platform.id)
