

from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface


class FindUserStep(StepSAGA):
    def __init__(self, user_name: str, repository: RepositoryInterface):
        """
        Initialize the CreateUserStep.

        Args:
            user (SignupEmailSchema): Data schema containing user signup information.
            session: Database session for interacting with the data.
        """
        self.user_name = user_name
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        """
        Execute the step, creating a user account.

        Args:
            payload: Not used in this step.

        Returns:
            UserModel: User object created during the step.
        """
        user = self.repository.get_by_attributes(filters={"user_name": self.user_name})
        if user is None:
            raise EntityNotFoundError(resource=self.user_name)

        return user

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
