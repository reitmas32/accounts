from shared.app.controllers.saga.controller import StepSAGA
from shared.app.enums.platform_login import PlatformsLogin
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface


class FindPlatformStep(StepSAGA):
    def __init__(
        self,
        external_id: str,
        platform: PlatformsLogin,
        repository: RepositoryInterface,
    ):
        self.external_id = external_id
        self.repository = repository
        self.platform = platform

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        platforms = self.repository.get_by_attributes(
            filters={
                "external_id": self.external_id,
                "platform": self.platform,
            },
        )
        if platforms is None or len(platforms) == 0:
            raise EntityNotFoundError(
                resource=f"platform with external id {self.external_id}"
            )

        return platforms[0]

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
