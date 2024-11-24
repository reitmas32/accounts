from typing import TYPE_CHECKING

from context.v1.emails.domain.steps.find import FindEmailStep
from shared.app.controllers.saga.controller import StepSAGA
from shared.app.enums.code_type import CodeTypeEnum
from shared.databases.errors.entity_not_found import EntityNotFoundError
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from context.v1.emails.domain.entities.email import EmailEntity


class FindLastCode(StepSAGA):
    def __init__(
        self,
        repository: RepositoryInterface,
        type_code: CodeTypeEnum
    ):
        self.repository = repository
        self.type_code = type_code

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        email: EmailEntity = all_payloads[FindEmailStep]


        codes = self.repository.get_by_attributes(
            filters={
                "entity_id": str(email.id),
                "type": self.type_code,
                "used_at": None
            },
        )
        if codes is None or len(codes) == 0:
            raise EntityNotFoundError(
                resource="There is no unused code active for the user"
            )

        return codes[0]

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
