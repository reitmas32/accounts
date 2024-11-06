from uuid import uuid4

from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.infrastructure.repository import RepositoryInterface


class CreateUserByUserNameStep(StepSAGA):
    def __init__(self, user_name: str, repository: RepositoryInterface):
        if user_name is None:
            user_name = f"User_{uuid4()}"
        self.user_name = user_name
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        self.user = None
        self.user = self.repository.add(user_name=self.user_name)
        return self.user

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
        if self.user is not None:
            self.repository.delete_by_id(self.user.id)
