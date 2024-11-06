from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface


class FindLoginMethodByPlatformStep(StepSAGA):
    def __init__(self, repository: RepositoryInterface):

        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002

        login_methods = self.repository.get_by_attributes(filters={"entity_id": str(payload.id)})
        if login_methods is None or len(login_methods) == 0:
            raise EntityNotFoundError(resource="login_method")

        return login_methods

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
