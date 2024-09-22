

from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.infrastructure.repository import RepositoryInterface


class SearchPlatformByExternalIdStep(StepSAGA):
    def __init__(self, external_id: str, repository: RepositoryInterface):

        self.external_id = external_id
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        platform = self.repository.get_by_attributes(filters={"external_id": self.external_id})
        if platform is None:
            return []

        return platform

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
