from shared.app.controllers.saga.controller import StepSAGA
from shared.app.enums.platform_login import PlatformsLogin
from shared.databases.infrastructure.repository import RepositoryInterface


class SearchPlatformStep(StepSAGA):
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
        platform = self.repository.get_by_attributes(
            filters={
                "external_id": self.external_id,
                "platform": self.platform,
            }
        )
        if platform is None or len(platform) == 0:
            return None

        return platform[0]

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
