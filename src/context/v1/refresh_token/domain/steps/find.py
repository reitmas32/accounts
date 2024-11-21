from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface


class FindEmailStep(StepSAGA):
    def __init__(
        self,
        email: str,
        repository: RepositoryInterface,
    ):
        self.email = email
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        emails = self.repository.get_by_attributes(
            filters={
                "email": self.email,
            },
        )
        if emails is None or len(emails) == 0:
            raise EntityNotFoundError(
                resource=f"User with Email {self.email} not found"
            )

        return emails[0]

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
