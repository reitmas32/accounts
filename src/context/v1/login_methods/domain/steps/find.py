from typing import TYPE_CHECKING

from shared.app.controllers.saga.controller import StepSAGA
from shared.app.errors.invalid.account_unverified import AccountUnverifiedError
from shared.app.errors.saga import SAGAError
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from context.v1.login_methods.domain.entities.login_method import LoginMethodEntity


class FindLoginMethodByPlatformStep(StepSAGA):
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        login_methods = self.repository.get_by_attributes(
            filters={"entity_id": str(payload.id)}
        )
        if login_methods is None or len(login_methods) == 0:
            raise EntityNotFoundError(resource="login_method")

        return login_methods

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """


class FindLoginMethodStep(StepSAGA):
    def __init__(self, find_step_type: type, repository: RepositoryInterface):
        self.find_step_type = find_step_type
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        entity = all_payloads.get(self.find_step_type)

        if entity is None:
            raise SAGAError(
                "Run FindEmailStep or FindPlatformStep before of FindLoginMethodStep"
            )

        login_methods: list[LoginMethodEntity] = self.repository.get_by_attributes(
            filters={"entity_id": str(entity.id)}
        )
        if login_methods is None or len(login_methods) == 0:
            raise EntityNotFoundError(resource="login_method")

        if not login_methods[0].verify:
            raise AccountUnverifiedError

        return login_methods[0]

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
