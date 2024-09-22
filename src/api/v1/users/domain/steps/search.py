

from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.infrastructure.repository import RepositoryInterface


class SearchUserByUserNameStep(StepSAGA):
    def __init__(self, user_name: str, repository: RepositoryInterface):

        self.user_name = user_name
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        users = self.repository.get_by_attributes(filters={"user_name": self.user_name})
        if users is None:
            return []

        return users

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
