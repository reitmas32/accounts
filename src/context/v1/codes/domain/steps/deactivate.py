from datetime import datetime
from typing import TYPE_CHECKING

from context.v1.codes.domain.steps.find_last import FindLastCode
from shared.app.controllers.saga.controller import StepSAGA
from shared.databases.infrastructure.repository import RepositoryInterface

if TYPE_CHECKING:
    from context.v1.codes.domain.entities.code import CodeEntity

class DeactivateCode(StepSAGA):
    def __init__(
        self,
        repository: RepositoryInterface,
    ):
        self.repository = repository

    def __call__(self, payload: None = None, all_payloads: dict | None = None):  # noqa: ARG002
        code: CodeEntity = all_payloads[FindLastCode]

        self.repository.update_field_by_id(code.id, "used_at", datetime.now().astimezone())

    def rollback(self):
        """
        Rollback the step, deleting the user account if it was created.
        """
